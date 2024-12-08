
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class a6 {

    public static Set<Position> numsteps(char[][] G, Position block) {
        int R = G.length;
        int C = G[0].length;

        State state = null;
        int[][] dirs = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
        int d = 0;

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (G[r][c] == '^') {
                    state = new State(r, c, d);
                }
            }
        }

        Set<State> SEEN = new HashSet();

        Set<Position> positions = new HashSet();

        do {
            if (state.r < 0 || state.r >= R || state.c < 0 || state.c >= C) {
                return positions;
            }

            if (SEEN.contains(state)) {
                return null;
            }
            SEEN.add(state);

            positions.add(new Position(state.r, state.c));

            while (true) {
                int nrow = state.r + dirs[d % 4][0];
                int ncol = state.c + dirs[d % 4][1];
                if (nrow >= 0 && nrow < R && ncol >= 0 && ncol < C) {
                    if (G[nrow][ncol] == '#' || (block != null && block.r == nrow && block.c == ncol)) {
                        d++;
                        continue;
                    }
                }

                state = new State(nrow, ncol, d%4);
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

        Set<Position> guardPositions = numsteps(G, null);
        System.out.println(guardPositions.size());

        ExecutorService executorService = Executors.newFixedThreadPool(4); // 4 threads
        List<Future<Set<Position>>> futures = new ArrayList();
        for (Position gp : guardPositions) {
            if (G[gp.r][gp.c] == '.') {
                futures.add(executorService.submit(() -> numsteps(G, new Position(gp.r, gp.c))));
            }
        }

        int p2 = 0;
        for (Future<Set<Position>> future : futures) {
            if (future.get() == null)
                p2++;
        }
        executorService.shutdownNow();
        
        System.out.println(p2);

    }
}

class Position {

    int r;
    int c;

    public Position(int r, int c) {
        this.c = c;
        this.r = r;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 13 * hash + this.r;
        hash = 13 * hash + this.c;
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Position other = (Position) obj;
        if (this.r != other.r) {
            return false;
        }
        return this.c == other.c;
    }

}

class State {

    int r;
    int c;
    int d;

    public State(int r, int c, int d) {
        this.c = c;
        this.d = d;
        this.r = r;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 29 * hash + this.r;
        hash = 29 * hash + this.c;
        hash = 29 * hash + this.d;
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final State other = (State) obj;
        if (this.r != other.r) {
            return false;
        }
        if (this.c != other.c) {
            return false;
        }
        return this.d == other.d;
    }

}
