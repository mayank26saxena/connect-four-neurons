/*
 * Connect Four bitboard engine and deterministic depth-limited teacher.
 *
 * Board layout (as in Pascal Pons' solver write-up): column-major, HEIGHT+1 bits per
 * column (top bit is a sentinel), bit index = col * (HEIGHT + 1) + row, row 0 at the bottom.
 * `pos` holds the stones of the player to move, `mask` holds all stones.
 *
 * Determinism: the teacher returns the exact depth-limited minimax value of every root move.
 * The transposition table is only used when the stored depth equals the requested depth,
 * so results never depend on search history, move order or table size.
 */
#include <stdint.h>
#include <string.h>

#define W 7
#define H 6
#define H1 (H + 1)
#define WIN_SCORE 1000
#define ILLEGAL (-32768)

typedef uint64_t u64;

static const u64 BOTTOM = 0x0000040810204081ULL; /* bit 0 of every column */
static const u64 BOARD = 0x0000040810204081ULL * ((1ULL << H) - 1);
static const int ORDER[W] = {3, 2, 4, 1, 5, 0, 6};

static inline u64 top_bit(int c) { return 1ULL << (H - 1 + c * H1); }
static inline u64 bottom_bit(int c) { return 1ULL << (c * H1); }
static inline u64 column_bits(int c) { return ((1ULL << H) - 1) << (c * H1); }
static inline int can_play(u64 mask, int c) { return (mask & top_bit(c)) == 0; }

static inline int popcount(u64 x) { return __builtin_popcountll(x); }

/* Empty cells where `p` would complete four in a row (Pons, compute_winning_position). */
u64 c4_winning_cells(u64 p, u64 mask) {
    u64 r = (p << 1) & (p << 2) & (p << 3);
    u64 t;
    t = (p << H1) & (p << 2 * H1);
    r |= t & (p << 3 * H1);
    r |= t & (p >> H1);
    t = (p >> H1) & (p >> 2 * H1);
    r |= t & (p << H1);
    r |= t & (p >> 3 * H1);
    t = (p << H) & (p << 2 * H);
    r |= t & (p << 3 * H);
    r |= t & (p >> H);
    t = (p >> H) & (p >> 2 * H);
    r |= t & (p << H);
    r |= t & (p >> 3 * H);
    t = (p << (H + 2)) & (p << 2 * (H + 2));
    r |= t & (p << 3 * (H + 2));
    r |= t & (p >> (H + 2));
    t = (p >> (H + 2)) & (p >> 2 * (H + 2));
    r |= t & (p << (H + 2));
    r |= t & (p >> 3 * (H + 2));
    return r & (BOARD ^ mask);
}

int c4_has_four(u64 p) {
    u64 m;
    m = p & (p >> H1); if (m & (m >> 2 * H1)) return 1;
    m = p & (p >> H); if (m & (m >> 2 * H)) return 1;
    m = p & (p >> (H + 2)); if (m & (m >> 2 * (H + 2))) return 1;
    m = p & (p >> 1); if (m & (m >> 2)) return 1;
    return 0;
}

static inline u64 playable(u64 mask) { return (mask + BOTTOM) & BOARD; }

/* Leaf heuristic from the point of view of the player to move (stones `pos`). */
static int heuristic(u64 pos, u64 mask) {
    u64 opp = pos ^ mask;
    u64 mine_w = c4_winning_cells(pos, mask);
    u64 opp_w = c4_winning_cells(opp, mask);
    u64 play = playable(mask);
    int s = 0;
    s += 4 * (popcount(mine_w) - popcount(opp_w));
    s += 2 * (popcount(mine_w & (play << 1)) - popcount(opp_w & (play << 1))); /* threats one cell above play */
    s += 1 * (popcount(pos & column_bits(3)) - popcount(opp & column_bits(3)));
    return s;
}

/* ---- transposition table (exact-depth hits only) ---- */
#define TT_BITS 22
#define TT_SIZE (1u << TT_BITS)
typedef struct { u64 key; int16_t val; int8_t depth; int8_t flag; } tt_entry;
static tt_entry TT[TT_SIZE];
enum { TT_EXACT = 1, TT_LOWER = 2, TT_UPPER = 3 };

void c4_tt_clear(void) { memset(TT, 0, sizeof(TT)); }

static long long NODES = 0;
long long c4_nodes(void) { return NODES; }

static int negamax(u64 pos, u64 mask, int ply, int depth, int alpha, int beta) {
    NODES++;
    /* immediate win for the side to move */
    u64 play = playable(mask);
    u64 mine_w = c4_winning_cells(pos, mask);
    if (play & mine_w) return WIN_SCORE - (ply + 1);
    if (ply >= W * H) return 0;
    if (depth == 0) return heuristic(pos, mask);

    u64 key = (pos + mask) * 0x9E3779B97F4A7C15ULL ^ (u64)depth;
    tt_entry *e = &TT[(key >> 17) & (TT_SIZE - 1)];
    int a0 = alpha;
    if (e->key == key && e->depth == depth) {
        if (e->flag == TT_EXACT) return e->val;
        if (e->flag == TT_LOWER && e->val > alpha) alpha = e->val;
        else if (e->flag == TT_UPPER && e->val < beta) beta = e->val;
        if (alpha >= beta) return e->val;
    }

    int best = -WIN_SCORE * 2;
    for (int i = 0; i < W; i++) {
        int c = ORDER[i];
        if (!can_play(mask, c)) continue;
        u64 nmask = mask | (mask + bottom_bit(c));
        u64 npos = pos ^ mask; /* opponent becomes side to move */
        int v = -negamax(npos, nmask, ply + 1, depth - 1, -beta, -alpha);
        if (v > best) best = v;
        if (v > alpha) alpha = v;
        if (alpha >= beta) break;
    }
    if (best == -WIN_SCORE * 2) best = 0; /* no moves: draw (full board) */

    e->key = key; e->depth = (int8_t)depth; e->val = (int16_t)best;
    e->flag = best <= a0 ? TT_UPPER : (best >= beta ? TT_LOWER : TT_EXACT);
    return best;
}

/* Replay a move sequence. Returns 0 on success, -1 on illegal move or move after a win. */
int c4_replay(const int8_t *moves, int n, u64 *pos_out, u64 *mask_out) {
    u64 pos = 0, mask = 0;
    for (int i = 0; i < n; i++) {
        int c = moves[i];
        if (c < 0 || c >= W || !can_play(mask, c)) return -1;
        if (c4_has_four(pos ^ mask)) return -1;
        pos ^= mask;
        mask |= mask + bottom_bit(c);
    }
    *pos_out = pos; *mask_out = mask;
    return 0;
}

/* Score every root move at the given depth. Illegal moves get ILLEGAL. */
int c4_score_moves(const int8_t *moves, int n, int depth, int16_t *scores) {
    u64 pos, mask;
    if (c4_replay(moves, n, &pos, &mask) != 0) return -1;
    for (int c = 0; c < W; c++) {
        if (!can_play(mask, c)) { scores[c] = ILLEGAL; continue; }
        u64 bit = (mask + bottom_bit(c)) & column_bits(c);
        if (c4_has_four(pos | bit)) { scores[c] = (int16_t)(WIN_SCORE - (n + 1)); continue; }
        u64 nmask = mask | bit;
        u64 npos = pos ^ mask;
        int v = -negamax(npos, nmask, n + 1, depth - 1, -WIN_SCORE * 2, WIN_SCORE * 2);
        scores[c] = (int16_t)v;
    }
    return 0;
}

/* Score every root move of an arbitrary bitboard (pos = stones of the player to move). ply = number of stones.
 * Used to evaluate edited boards; returns -1 if either side already has four. */
int c4_score_board(u64 pos, u64 mask, int depth, int16_t *scores) {
    if (c4_has_four(pos) || c4_has_four(pos ^ mask)) return -1;
    int n = popcount(mask);
    for (int c = 0; c < W; c++) {
        if (!can_play(mask, c)) { scores[c] = ILLEGAL; continue; }
        u64 bit = (mask + bottom_bit(c)) & column_bits(c);
        if (c4_has_four(pos | bit)) { scores[c] = (int16_t)(WIN_SCORE - (n + 1)); continue; }
        int v = -negamax(pos ^ mask, mask | bit, n + 1, depth - 1, -WIN_SCORE * 2, WIN_SCORE * 2);
        scores[c] = (int16_t)v;
    }
    return 0;
}

/* ---- deterministic RNG ---- */
static inline u64 splitmix(u64 *s) {
    u64 z = (*s += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
/*
 * exp(x) for x <= 0 using only IEEE + - * / (correctly rounded on every platform), so that
 * sampled games are bit-identical across compilers and C libraries (libm exp is not).
 */
static double det_exp(double x) {
    if (x < -700.0) return 0.0;
    int k = 0;
    while (x < -0.5) { x += 0.6931471805599453; k++; } /* x = r - k ln2 */
    double term = 1.0, sum = 1.0;
    for (int i = 1; i < 25; i++) { term = term * x / (double)i; sum += term; }
    while (k-- > 0) sum *= 0.5;
    return sum;
}

static inline double uniform(u64 *s) { return (double)(splitmix(s) >> 11) * (1.0 / 9007199254740992.0); }

/*
 * Play one game. The first `random_plies` plies are uniform random; later plies are sampled
 * from softmax(scores / temp) (temp <= 0 means argmax with lowest-column tie break).
 * Writes moves[0..n-1] and scores[t*7 + c] for every position t in 0..n-1 (position before move t).
 * Returns n; *result = 1 (first player won), 2 (second player won), 0 (draw).
 */
int c4_gen_game(u64 seed, int depth, double temp, int random_plies, int8_t *moves, int16_t *scores, int *result) {
    u64 rng = seed;
    u64 pos = 0, mask = 0;
    int n = 0;
    *result = 0;
    while (n < W * H) {
        int16_t *sc = scores + n * W;
        c4_score_moves(moves, n, depth, sc);
        int c = -1;
        if (n < random_plies) {
            int legal[W], k = 0;
            for (int j = 0; j < W; j++) if (can_play(mask, j)) legal[k++] = j;
            c = legal[splitmix(&rng) % (u64)k];
        } else if (temp <= 0) {
            int bv = ILLEGAL;
            for (int j = 0; j < W; j++) if (sc[j] != ILLEGAL && sc[j] > bv) { bv = sc[j]; c = j; }
        } else {
            double mx = -1e9, p[W], z = 0;
            for (int j = 0; j < W; j++) if (sc[j] != ILLEGAL && sc[j] > mx) mx = sc[j];
            for (int j = 0; j < W; j++) { p[j] = sc[j] == ILLEGAL ? 0.0 : det_exp((sc[j] - mx) / temp); z += p[j]; }
            double u = uniform(&rng) * z, acc = 0;
            for (int j = 0; j < W; j++) { if (p[j] == 0) continue; acc += p[j]; c = j; if (u < acc) break; }
        }
        u64 bit = (mask + bottom_bit(c)) & column_bits(c);
        int won = c4_has_four(pos | bit);
        moves[n++] = (int8_t)c;
        pos ^= mask;
        mask |= bit;
        if (won) { *result = (n % 2 == 1) ? 1 : 2; break; }
    }
    return n;
}
