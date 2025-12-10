#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cstdint>
#include <bitset>
#include <queue>
#include <algorithm>
#include <unordered_set>
#include <optional>
#include <functional>
#include <limits>

using namespace std;

/**
 * Converts a bitmap string of '.' and '#' characters into a 16-bit value.
 *
 * The least significant bit corresponds to the **rightmost** character.
 * A '.' represents a 0 bit, and a '#' represents a 1 bit.
 *
 * Example:
 *   parseBitmap("[.#..]")  // '#' → bit 1 = 1, others 0
 *
 * @param s A string consisting of '.' and '#' characters.
 * @return  A 16-bit bitmap representing the pattern in the string.
 */
uint16_t parseBitmap(const string& s) {
    string aux_s = s;
    reverse(aux_s.begin(), aux_s.end());
    uint16_t value = 0;
    for (char c : aux_s) {
        value <<= 1;
        if (c == '#') value |= 1;
    }
    return value;
}

/**
 * Constructs a 16-bit mask from a list of bit indices.
 *
 * Each index in the vector specifies a bit position (0–15)
 * that should be set to 1 in the resulting mask.
 *
 * Example:
 *   makeMask({0, 3, 5})  // produces a mask with bits 0,3,5 set
 *
 * @param bits A vector of bit positions to enable (range 0–15).
 * @return     A 16-bit mask with the specified bits set to 1.
 */
uint16_t makeMask(const vector<uint16_t>& bits) {
    uint16_t mask = 0;
    for (int b : bits) {
        if (b >= 0 && b < 16)
            mask |= (1u << b);
    }
    return mask;
}

/**
 * Computes the minimum number of bitmask applications required to
 * transform an initial 0-bitmask into the desired bitmask.
 *
 * Each mask represents an XOR operation that can be applied once
 * per step. The function performs a BFS over all 16-bit states
 * to find the shortest sequence of XOR operations that reaches
 * the desired state.
 *
 * @param desired The target 16-bit bitmap to reach.
 * @param masks   The list of XOR masks that may be applied.
 * @return        The minimum number of steps required, or -1 if unreachable.
 */
int solveMinXorSteps(const uint16_t desired, const vector<uint16_t>& masks) {
    static int dist[65536];

    for (int i = 0; i < 65536; i++) dist[i] = -1;

    queue<uint16_t> q;
    q.push(0);
    dist[0] = 0;

    while (!q.empty()) {
        uint16_t cur = q.front();
        q.pop();

        if (cur == desired)
            return dist[cur];

        for (uint16_t mask : masks) {
            uint16_t next = cur ^ mask;

            // unvisited
            if (dist[next] == -1) {
                dist[next] = dist[cur] + 1;
                q.push(next);
            }
        }
    }

    // something went wrong
    return -1;
}

/**
 * Solves for the minimum number of button presses required to reproduce
 * the target values using a linear system derived from button–position
 * dependencies.
 *
 * Each button contributes +1 to the positions listed in its index set.
 * The goal is to find non-negative integer press counts for each button
 * such that the cumulative contributions match the desired vector, while
 * minimizing the total number of presses.
 *
 * The function constructs the linear system:
 *
 *     A * x = desired
 *
 * where:
 *   - A[i][j] = 1 if button j affects position i, else 0
 *   - x[j]    = number of times button j is pressed (variables)
 *   - desired[i] = required total increments at position i
 *
 * Gauss–Jordan elimination is used to compute a reduced system, after
 * which free variables are enumerated (with bounded search) to find the
 * integer solution with minimal total press count.
 *
 * @param desired  A vector of target values for each position.
 * @param buttons  A list of buttons, where each button is a list of
 *                 positions it increments when pressed once.
 *
 * @return The minimal total number of presses needed to satisfy the
 *         system, or -1 if no non-negative integer solution exists.
 */
int solveMinPressesLinearSystem(const vector<uint16_t>& desired, const vector<vector<uint16_t>>& buttons) {
    // WARNING: this solution does not work but it was interesting to implement
    int n = desired.size();
    int m = buttons.size();

    // Build augmented matrix [A | b]
    vector<vector<long long>> M(n, vector<long long>(m + 1, 0));
    for (int j = 0; j < m; j++) {
        for (uint16_t idx : buttons[j])
            M[idx][j] = 1;
    }
    for (int i = 0; i < n; i++)
        M[i][m] = desired[i];

    // Gauss-Jordan elimination to RREF
    int row = 0;
    vector<int> pivot_col(m, -1);

    for (int col = 0; col < m && row < n; col++) {
        // Find non-zero pivot
        int sel = row;
        while (sel < n && M[sel][col] == 0) sel++;
        if (sel == n) continue;

        swap(M[sel], M[row]);

        long long pivot = M[row][col];
        // Make pivot = 1
        for (int j = col; j <= m; j++)
            M[row][j] /= pivot;

        // Eliminate column in all other rows
        for (int i = 0; i < n; i++) {
            if (i != row && M[i][col] != 0) {
                long long factor = M[i][col];
                for (int j = col; j <= m; j++)
                    M[i][j] -= factor * M[row][j];
            }
        }

        pivot_col[col] = row;
        row++;
    }

    // Check for inconsistent system
    for (int i = 0; i < n; i++) {
        bool allZero = true;
        for (int j = 0; j < m; j++)
            if (M[i][j] != 0) allZero = false;
        if (allZero && M[i][m] != 0)
            return -1;
    }

    // Identify free variables (non-pivot columns)
    vector<int> free_vars;
    for (int j = 0; j < m; j++) {
        if (pivot_col[j] == -1)
            free_vars.push_back(j);
    }

    // If no free variables, compute the unique solution
    if (free_vars.empty()) {
        long long cost = 0;
        for (int col = 0; col < m; col++) {
            if (pivot_col[col] != -1) {
                int r = pivot_col[col];
                long long val = M[r][m];
                if (val < 0) return -1;
                cost += val;
            }
        }
        return (int)cost;
    }

    // Calculate upper bound: sum of all desired values is an upper bound
    long long max_possible = 0;
    for (auto v : desired) max_possible += v;
    
    int search_bound = min(500LL, max_possible);

    long long best = numeric_limits<long long>::max();
    vector<long long> candidate(m, 0);

    // Enumerate free variable assignments (DFS with pruning)
    function<void(int)> dfs = [&](int k) {
        // stop if current free vars already exceed best
        long long current_free_sum = 0;
        for (int i = 0; i < k; i++) {
            current_free_sum += candidate[free_vars[i]];
        }
        if (current_free_sum >= best) return;
        
        if (k == (int)free_vars.size()) {
            vector<long long> x(m, 0);

            // Set free variables
            for (int i = 0; i < (int)free_vars.size(); i++) {
                x[free_vars[i]] = candidate[free_vars[i]];
            }

            // Back-substitute to solve for pivot variables
            for (int col = m - 1; col >= 0; col--) {
                if (pivot_col[col] != -1) {
                    int r = pivot_col[col];
                    long long val = M[r][m];
                    for (int j = col + 1; j < m; j++) {
                        val -= M[r][j] * x[j];
                    }
                    if (val < 0) return; // Must be non-negative
                    x[col] = val;
                }
            }

            // Compute total cost
            long long cost = 0;
            for (long long v : x) cost += v;
            if (cost < best) best = cost;

            return;
        }

        int var = free_vars[k];
        // Try values up to search bound
        for (int t = 0; t <= search_bound; t++) {
            candidate[var] = t;
            dfs(k + 1);
        }
    };

    dfs(0);

    return (best == numeric_limits<long long>::max() ? -1 : (int)best);
}

int main() {
    ifstream fin("../input.in");
    string line;
    int part1_total = 0;
    int part2_total = 0;
    
    while (getline(fin, line)) {
        stringstream ss(line);
        string token;

        // Parse initial bitmap [...]
        ss >> token;
        string bitmap_str = token.substr(1, token.size() - 2);
        uint16_t initial_bitmap = parseBitmap(bitmap_str);

        // Parse button definitions (...)
        vector<uint16_t> button_masks;
        vector<vector<uint16_t>> button_positions;

        while (ss >> token) {
            if (token[0] == '{') break; // Reached target values
            if (token[0] != '(') continue;
            
            // Handle multi-token parentheses if needed
            if (token.back() != ')') {
                string continuation;
                while (ss >> continuation) {
                    token += continuation;
                    if (continuation.back() == ')') break;
                }
            }

            // Extract position indices from (...)
            string positions_str = token.substr(1, token.size() - 2);
            vector<uint16_t> positions;

            if (!positions_str.empty()) {
                stringstream position_stream(positions_str);
                string position;
                while (getline(position_stream, position, ',')) {
                    positions.push_back(stoi(position));
                }
            }
            
            button_positions.push_back(positions);
            button_masks.push_back(makeMask(positions));
        }

        // Parse target joltage {...}
        string target_str = token.substr(1, token.size() - 2);
        vector<uint16_t> target_values;
        
        stringstream target_stream(target_str);
        string value;
        while (getline(target_stream, value, ',')) {
            target_values.push_back(stoi(value));
        }

        // Solve both parts
        part1_total += solveMinXorSteps(initial_bitmap, button_masks);
        part2_total += solveMinPressesLinearSystem(target_values, button_positions);
    }
    
    cout << part1_total << ' ' << part2_total << '\n';
}
