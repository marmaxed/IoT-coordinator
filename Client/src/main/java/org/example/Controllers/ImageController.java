package org.example.Controllers;

import lombok.SneakyThrows;

import org.springframework.core.io.InputStreamResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import javax.script.*;
import java.io.*;
import java.nio.file.Files;
import java.util.List;


@Controller
public class ImageController {

    @SneakyThrows
    public void executeScript(Object[] values) throws FileNotFoundException, ScriptException {
        List<Float> vals = (List<Float>) values[0];
        List<Long> times = (List<Long>) values[1];
        String t = times.toString();
        t = t.replaceAll(",","");
        t=t.substring(1, t.length()-1);
        String v = vals.toString();
        v = v.replaceAll(",","");
        v=v.substring(1, v.length()-1);
        System.out.println(t+"\n"+v);
        System.out.println("hih");
        Process p = Runtime.getRuntime().exec(String.format("python src/main/resources/script.py -v %s -k %s",t,v));
        BufferedReader stdInput = new BufferedReader(new
                InputStreamReader(p.getInputStream()));
        System.out.println("Here is the standard output of the command:\n");
        for (String s:stdInput.lines().toList()) {
            System.out.println(s);
        }
    }

    @SneakyThrows
    public void executePersonalScript(Object[] values, int ID) throws FileNotFoundException, ScriptException {
        List<Float> vals = (List<Float>) values[0];
        List<Long> times = (List<Long>) values[1];
        String t = times.toString();
        t = t.replaceAll(",","");
        t=t.substring(1, t.length()-1);
        String v = vals.toString();
        v = v.replaceAll(",","");
        v=v.substring(1, v.length()-1);
        System.out.println(t+"\n"+v);
        System.out.println("hih");
        Process p = Runtime.getRuntime().exec(String.format("python src/main/resources/personal.py -v %s -k %s -id %s",t,v,ID));
        BufferedReader stdInput = new BufferedReader(new
                InputStreamReader(p.getInputStream()));
        System.out.println("Here is the standard output of the command:\n");
        for (String s:stdInput.lines().toList()) {
            System.out.println(s);
        }
    }

    @SneakyThrows
    @GetMapping("/images")
    private ResponseEntity<?> getImageById(){
        File image = new File("src/main/resources/script.png");
        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_PNG)
                .contentLength(image.length())
                .body(new InputStreamResource(new ByteArrayInputStream(Files.readAllBytes(image.toPath()))));
    }

    /*@SneakyThrows
    @GetMapping("/images")
    private ResponseEntity<?> getImageById(){
        File image = new File("src/main/resources/script.png");
        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_PNG)
                .contentLength(image.length())
                .body(new InputStreamResource(new ByteArrayInputStream(Files.readAllBytes(image.toPath()))));
    }*/

    @SneakyThrows
    @GetMapping("/reload")
    private ResponseEntity<?> getReoloadImg(){
        File image = new File("src/main/resources/reload.png");
        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_PNG)
                .contentLength(image.length())
                .body(new InputStreamResource(new ByteArrayInputStream(Files.readAllBytes(image.toPath()))));
    }

}
