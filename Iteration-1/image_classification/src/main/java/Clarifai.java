import clarifai2.api.ClarifaiBuilder;
import clarifai2.api.ClarifaiClient;
import clarifai2.api.ClarifaiResponse;
import clarifai2.dto.input.ClarifaiInput;
import clarifai2.dto.input.image.ClarifaiImage;
import clarifai2.dto.model.output.ClarifaiOutput;
import clarifai2.dto.prediction.Concept;
import okhttp3.OkHttpClient;

import java.io.File;
import java.io.IOException;
import java.util.List;

/**
 * Created by Raj on 02-05-2017.
 */
public class Clarifai {
    public static String testImage(String img) throws IOException {

        //final ClarifaiClient client = new ClarifaiBuilder("cT-RYP0YjP0jlO4ASrLyPoGP768jOVD6mUfmoMDr", "sZ2vVaKHKdyFITb0BLLXTa0f9qOh86UoAO_uub6K")
        final ClarifaiClient client = new ClarifaiBuilder("xSj3UtS7J9397wku4XwCjfJVb2dYUaF7U5rIkacQ", "ujp7e5O7llwf_PHpcE-KMcyhQrABU_cMsl24Ubp8")
                .client(new OkHttpClient())
                .buildSync();
        client.getToken();

        //Use the custom model Mouth-Sore to predict the image
         ClarifaiResponse response = client.predict("Mouth-Sore")
                .withInputs(
                        ClarifaiInput.forImage(ClarifaiImage.of(new File(img)))
                )
                .executeSync();
        List<ClarifaiOutput<Concept>> predictions = (List<ClarifaiOutput<Concept>>) response.get();

        String retval = "";

        if (predictions.isEmpty()) {
            retval = "You are pulling my leg. I don't see any sores. You are good!";
        }
        else{
            List<Concept> data = predictions.get(0).data();

            String Sore_name = "";
            float Sore_value = 0;

            for (int i = 0; i < data.size(); i++) {
                System.out.println(data.get(i).name() + " - " + data.get(i).value());
                if (data.get(i).value() > Sore_value) {
                    Sore_value = data.get(i).value();
                    Sore_name = data.get(i).name();
                }
            }

            retval = "There is a " + String.format("%.2f", Sore_value*100) + "% chance that this is a " + Sore_name + ".";

        }
        return retval;
    }
}
