
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

public class a6 {

    private static Set<Position> calculatePositions(char[][] G, Position block) {
        int R = G.length;
        int C = G[0].length;

        State state = null;
        int[][] dirs = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
        int d = 0;

        l1:
        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (G[r][c] == '^') {
                    state = new State(r, c, d);
                    break l1;
                }
            }
        }

        Set<State> SEEN = new HashSet();

        Set<Position> positions = new HashSet();

        do {
            if (state.r() < 0 || state.r() >= R || state.c() < 0 || state.c() >= C) {
                return positions;
            }

            if (!SEEN.add(state)) {
                return null;
            }

            positions.add(new Position(state.r(), state.c()));

            while (true) {
                int nrow = state.r() + dirs[d % 4][0];
                int ncol = state.c() + dirs[d % 4][1];
                if (nrow >= 0 && nrow < R && ncol >= 0 && ncol < C) {
                    if (G[nrow][ncol] == '#' || (block != null && block.r() == nrow && block.c() == ncol)) {
                        d++;
                        continue;
                    }
                }

                state = new State(nrow, ncol, d % 4);
                break;
            }

        } while (true);
    }

    public static void main(String[] args) throws Exception {
        // Read file a6.txt as input string
        List<String> Gs = Files.readAllLines(Paths.get("6.txt"), Charset.defaultCharset());

        char[][] G = new char[Gs.size()][];
        for (int r = 0; r < Gs.size(); r++) {
            G[r] = Gs.get(r).toCharArray();
        }

        Set<Position> guardPositions = calculatePositions(G, null);
        int p1 = guardPositions.size();
        System.out.println(p1);

        long p2 = guardPositions.parallelStream()
                .filter(gp -> G[gp.r()][gp.c()] == '.')
                .map(gp -> calculatePositions(G, new Position(gp.r(), gp.c())))
                .filter(Objects::isNull)
                .count();

        System.out.println(p2);
    }
}

record Position(int r, int c) {

}

record State(int r, int c, int d) {

}
