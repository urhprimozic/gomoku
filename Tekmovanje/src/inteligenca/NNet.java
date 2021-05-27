package inteligenca;

import java.io.IOException;
import java.nio.file.Paths;

import ai.djl.Device;
import ai.djl.MalformedModelException;
import ai.djl.Model;
import ai.djl.inference.Predictor;
import ai.djl.ndarray.NDArray;
import ai.djl.ndarray.NDList;
import ai.djl.ndarray.NDManager;
import ai.djl.translate.Batchifier;
import ai.djl.translate.TranslateException;
import ai.djl.translate.Translator;
import ai.djl.translate.TranslatorContext;
import logika.Board;
import logika.Pair;

public class NNet {
	protected Model model;
	protected Predictor<float[][], Pair<float[], Float>> predictor;
		
	public NNet() {
	
		model = Model.newInstance("GomokuNNet");
		try {
			model.load(Paths.get(""));
		} catch (MalformedModelException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Translator<float[][], Pair<float[], Float>> translator = new Translator<float[][], Pair<float[], Float>>() {
			@Override
			public NDList processInput(TranslatorContext ctx, float[][] input) {
				NDManager manager = ctx.getNDManager();
				NDArray array = manager.create(input);
				return new NDList(array);
			}
			
			@Override
			public Pair<float[], Float> processOutput(TranslatorContext ctx, NDList list) {
				float[] vals = list.get(0).toFloatArray();
				for (int j = 0; j < vals.length; ++j) {
					vals[j] *= -1;
				}
				float v = list.get(1).toFloatArray()[0];
				return new Pair<float[], Float>(vals, v);
			}
	
			@Override
			public Batchifier getBatchifier() {
				return Batchifier.STACK;
			}
		};
		
		predictor = model.newPredictor(translator);
	}
	
	
	public Pair<float[], Float> predict(Board b) {	
		float[][] inp = new float[b.n][b.n];
		for (int i = 0; i < b.n; ++i) {
			for (int j = 0; j < b.n; ++j) {
				inp[i][j] = (float) b.plosca[i][j];
			}
		}
		
		try {
			return predictor.predict(inp);
		} catch (TranslateException e) {
			float[] arr = new float[b.n*b.n];
			for (int i = 0; i < b.n*b.n; ++i) {
				arr[i] = (float) Math.random();
			}
			return new Pair<float[], Float>(arr, (float) (2*Math.random()-1));
		}
		
	}
}
