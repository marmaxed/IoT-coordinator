package org.example.Utils;

import java.sql.Timestamp;
import java.time.*;
import java.util.Date;

public class TimeUtils {

    public static long getTime(String date, int hours, int min) {
        String[] vals = date.split("-");
        int year = Integer.parseInt(vals[0]);
        int mounth = Integer.parseInt(vals[1]);
        int day = Integer.parseInt(vals[2]);
        Date date1 = new Date(year-1900,mounth-1,day,hours,min);
        System.out.println(date1);
        System.out.println(date1.getTime()/1000);
        return date1.getTime()/1000;
    }
}
