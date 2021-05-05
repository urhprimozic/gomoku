package montecarlo;

import java.util.Collections;
import java.util.Comparator;

public class UCT {
	public static double uctValue(int totalVisit, double nodeWinScore, int nodeVisit) {
		return ((double) nodeWinScore / (double) nodeVisit) + 1.41 * Math.sqrt(Math.log(totalVisit) / (double) nodeVisit);
	}

	public static Node findBestNodeWithUCT(Node node) {
		int parentVisit = node.state.visitCount;
		return Collections.max(node.childArray, Comparator.comparing(c -> uctValue(parentVisit, c.state.winScore, c.state.visitCount)));
	}

}
