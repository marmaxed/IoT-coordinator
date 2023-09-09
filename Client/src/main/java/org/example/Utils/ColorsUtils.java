package org.example.Utils;

import org.example.Models.Sensor;

public class ColorsUtils {

    private static final int HUM_LEVEL=100/10;
    private static final int LIGHT_LEVEL=666/10;
    private static final int TEMP_LEVEL=50/10;

    private static String[] humColor = new String[10];
    private static String[] lightColor = new String[10];
    private static String[] tempColor = new String[10];

    static {
        humColor[0]="rgba(111, 66, 193, 0.1)";
        humColor[1]="rgba(111, 66, 193, 0.2)";
        humColor[2]="rgba(111, 66, 193, 0.3)";
        humColor[3]="rgba(111, 66, 193, 0.4)";
        humColor[4]="rgba(111, 66, 193, 0.5)";
        humColor[5]="rgba(111, 66, 193, 0.6)";
        humColor[6]="rgba(111, 66, 193, 0.7)";
        humColor[7]="rgba(111, 66, 193, 0.8)";
        humColor[8]="rgba(111, 66, 193, 0.9)";
        humColor[9]="rgba(111, 66, 193, 1)";
        lightColor[0]="rgba(13, 202, 240, 0.1)";
        lightColor[1]="rgba(13, 202, 240, 0.2)";
        lightColor[2]="rgba(13, 202, 240, 0.3)";
        lightColor[3]="rgba(13, 202, 240, 0.4)";
        lightColor[4]="rgba(13, 202, 240, 0.5)";
        lightColor[5]="rgba(13, 202, 240, 0.6)";
        lightColor[6]="rgba(13, 202, 240, 0.7)";
        lightColor[7]="rgba(13, 202, 240, 0.8)";
        lightColor[8]="rgba(13, 202, 240, 0.9)";
        lightColor[9]="rgba(13, 202, 240, 1);";
        tempColor[0]="rgba(32, 201, 151, 0.1)";
        tempColor[1]="rgba(32, 201, 151, 0.2)";
        tempColor[2]="rgba(32, 201, 151, 0.3)";
        tempColor[3]="rgba(32, 201, 151, 0.4)";
        tempColor[4]="rgba(32, 201, 151, 0.5)";
        tempColor[5]="rgba(32, 201, 151, 0.6)";
        tempColor[6]="rgba(32, 201, 151, 0.7)";
        tempColor[7]="rgba(32, 201, 151, 0.8)";
        tempColor[8]="rgba(32, 201, 151, 0.9)";
        tempColor[9]="rgba(32, 201, 151, 1)";
    }

    public static void setColor(Sensor sensor) {
        switch (sensor.getType()) {
            case LIGHT_SENSOR -> {
                int index = (int) sensor.getValue()/LIGHT_LEVEL;
                try {
                    sensor.setColor(lightColor[index]);
                } catch (ArrayIndexOutOfBoundsException e) {
                    sensor.setColor(lightColor[9]);
                }
            }
            case HUMIDITY_SENSOR -> {
                int index = (int) sensor.getValue()/HUM_LEVEL;
                System.out.println(index);
                System.out.println(sensor.getValue());
                System.out.println(HUM_LEVEL);
                try {
                    sensor.setColor(humColor[index]);
                }
                catch (ArrayIndexOutOfBoundsException e) {
                    sensor.setColor(humColor[9]);
                }
            }
            case TEMPERATURE_SENSOR -> {
                int index = (int) sensor.getValue()/TEMP_LEVEL;
                try {
                    sensor.setColor(tempColor[index]);
                } catch (ArrayIndexOutOfBoundsException e) {
                    sensor.setColor(tempColor[9]);
                }

            }
            default -> sensor.setColor("#fd7e14");
        }
    }
}
