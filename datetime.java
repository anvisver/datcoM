import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

public class datetime {

    public static void main(String[] args) {
        
        String content = "{2007,7,19}";

        Dat.setBaseValues(new int[] {0,1,1});

        Dat b = Dat.datetime("2026,2,25,10,37", Dat.AC, false);

        Dat a = Dat.datetime(content, Dat.AC, false);

        System.out.println(a.sub(b));
        
    }
}


class DatConv {

    public List<Double> output = new ArrayList<>();
    protected double rawtime;
    protected static int[] min_clock_value = {1,1,1};
    
    private int converter;
    

    public DatConv() {
        converter = 0;
    }


    public Dat _convert_to_() {
        converter = 1;
        return (Dat) this;
    }

    public Dat _object_only_accounts_for() {
        converter = 2;
        return (Dat) this;
    }

    public Object year() {
        if (converter == 1) {
            return seconds_to_exact_years(this.rawtime);
        } else if (converter == 2) {
            return Dat.datetime(String.valueOf(this.output.get(0)), Dat.AC, false);
        }
        return this.output.get(0);
    }

    public Object month() {
        if (this.converter == 1) {
            return seconds_to_exact_months((int) this.rawtime);
        }
        if (this.converter == 2) {
            String select = 1 + "," + this.output.get(1);
            return Dat.datetime(select, Dat.AC, false);
        }
        return this.output.get(1);
    }

    public Object day() {
        if (this.converter == 1) {
            return seconds_to_days((Double) this.rawtime);
        }
        if (this.converter == 2) {
            String select = 1 + "," + 1 + "," + this.output.get(2);
            return Dat.datetime(select, Dat.AC, false);
        }
        return this.output.get(2);
    }

    public Object hour() {
        if (this.converter == 1) {
            return this.rawtime / 3600;
        }
        if (this.converter == 2) {
            return Dat.datetime(new double[]{1, 1, 1, this.output.get(3)}, Dat.AC, false);
        }
        return this.output.get(3);
    }

    public Object minute() {
        if (this.converter == 1) {
            return this.rawtime / 60;
        } else if (this.converter == 2) {
            return Dat.datetime(new double[]{1, 1, 1, 0, this.output.get(4)}, Dat.AC, false);
        }
        return this.output.get(4);
    }

    public Object second() {
        if (this.converter == 1) {
            return this.rawtime;
        } else if (this.converter == 2) {
            return Dat.datetime(new double[]{1, 1, 1, 0, 0, this.output.get(5)}, Dat.AC, false);
        }
        return this.output.get(5);
    }

    private double seconds_to_days(double seconds) {
        final int SECONDS_PER_DAY = 24 * 60 * 60;
        return seconds / SECONDS_PER_DAY;
    }

    private static int seconds_in_month(int year, int month) {

        Dict baseline = new Dict(null);
        baseline.add(1, 31);
        baseline.add(3, 31);
        baseline.add(5, 31);
        baseline.add(7, 31);
        baseline.add(8, 31);
        baseline.add(10, 31);
        baseline.add(12, 31);

        baseline.add(4, 30);
        baseline.add(6, 30);
        baseline.add(9, 30);
        baseline.add(11, 30);

        baseline.add(2, is_leap_year(year) ? 29 : 28);

        int value;
        try {
            value = (int) baseline.pull(month);  // FIXED (was year)
        } catch (Exception e) {
            return 0;
        }

        return value * 24 * 60 * 60;
    }

    private static double seconds_to_exact_months(int seconds) {
        int year = 0;
        int month = 1;
        int month_passed = 0;

        while (seconds >= seconds_in_month(year, month)) {
            seconds -= seconds_in_month(year, month);
            month_passed += 1;
            month += 1;
            if (month > 12) {
                month = 1;
                year += 1;
            }
        }

        double fraction_of_month = (double) seconds / seconds_in_month(year, month);
        return month_passed + fraction_of_month;
    }

    private static boolean is_leap_year(int y) {
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }

    private static int seconds_in_year(int y) {
        int days = is_leap_year(y) ? 366 : 365;
        return days * 24 * 60 * 60;
    }

    private static double seconds_to_exact_years(double seconds) {
        int year_passed = 0;
        int year = 0;

        while (seconds >= seconds_in_year(year)) {
            seconds -= seconds_in_year(year);
            year += 1;
            year_passed += 1;
        }

        double fraction_of_year = seconds / seconds_in_year(year);
        return year_passed + fraction_of_year;
    }
}
class DatMath extends DatConv {


    public DatMath() {}

    /* ===================== ADD ===================== */

    public Dat add(DatMath other) {
        return Dat.operand(this.rawtime + other.rawtime);
    }

    public Dat add(double seconds) {
        return Dat.operand(this.rawtime + seconds);
    }

    /* ===================== SUB ===================== */

    public Dat sub(DatMath other) {
        return Dat.operand(this.rawtime - other.rawtime);
    }

    public Dat sub(double seconds) {
        return Dat.operand(this.rawtime - seconds);
    }

    /* ===================== MUL ===================== */

    public Dat mul(DatMath other) {
        return Dat.operand(this.rawtime * other.rawtime);
    }

    public Dat mul(double value) {
        return Dat.operand(this.rawtime * value);
    }

    /* ===================== DIV ===================== */

    public Dat div(DatMath other) {
        return Dat.operand(this.rawtime / other.rawtime);
    }

    public Dat div(double value) {
        return Dat.operand(this.rawtime / value);
    }

    /* ===================== FLOOR DIV ===================== */

    public Dat floordiv(DatMath other) {
        return Dat.operand(Math.floor(this.rawtime / other.rawtime));
    }

    public Dat floordiv(double value) {
        return Dat.operand(Math.floor(this.rawtime / value));
    }

    /* ===================== MOD ===================== */

    public double mod(DatMath other) {
        return this.rawtime % other.rawtime;
    }

    public double mod(double value) {
        return this.rawtime % value;
    }

    /* ===================== POW ===================== */

    public Dat pow(DatMath other) {
        return Dat.operand(Math.pow(this.rawtime, other.rawtime));
    }

    public Dat pow(double value) {
        return Dat.operand(Math.pow(this.rawtime, value));
    }

    /* ===================== COMPARISONS ===================== */

    public boolean eq(DatMath other) {
        return this.rawtime == other.rawtime;
    }

    public boolean eq(double value) {
        return this.rawtime == value;
    }

    public boolean gt(DatMath other) {
        return this.rawtime > other.rawtime;
    }

    public boolean gt(double value) {
        return this.rawtime > value;
    }

    public boolean ge(DatMath other) {
        return this.rawtime >= other.rawtime;
    }

    public boolean ge(double value) {
        return this.rawtime >= value;
    }

    public boolean lt(DatMath other) {
        return this.rawtime < other.rawtime;
    }

    public boolean lt(double value) {
        return this.rawtime < value;
    }

    public boolean le(DatMath other) {
        return this.rawtime <= other.rawtime;
    }

    public boolean le(double value) {
        return this.rawtime <= value;
    }

    public boolean ne(DatMath other) {
        return this.rawtime != other.rawtime;
    }

    public boolean ne(double value) {
        return this.rawtime != value;
    }
}
class Dat extends DatMath {

    private static boolean INNUMBERS(char c) {
        return (c >= '0' && c <= '9') || c == '.';
    }
    protected enum EpochType { AC, BC }
    final static public EpochType AC = EpochType.AC;
    final static public EpochType BC = EpochType.BC;

    private static final String[] bs_template = {"y", "m", "d", "h", "mi", "s"};
    protected EpochType epoch_type;

    public Dat() {
        super();
    }

    @Override
    public String toString() {
        int Y = this.output.get(0).intValue();
        int M = this.output.get(1).intValue();
        int D = this.output.get(2).intValue();
        int h = this.output.get(3).intValue();
        int mi = this.output.get(4).intValue();
        long s = Math.round(this.output.get(5));

        String epochType = (this.rawtime < 0) ? BC.name() : AC.name();

        return String.format("(%04d-%02d-%02d %02d:%02d:%02d)%s", Y, M, D, h, mi, s, epochType);

    }
    
    //getters

    public long getRawtime(){
        
        return (long) rawtime;
    }

    public static void setBaseValues(int[] values){
        min_clock_value = values;
    }

    public static Dat datetime(String rawinputvalue, EpochType epochType, boolean template_reverse) {
        Dat self = new Dat();
        List<Double> value = Dat.value_extractor(rawinputvalue);
        self.epoch_type = epochType;
        String[] template = template_reverse ? new String[]{"s", "mi", "h", "d", "m", "y"} : new String[]{"y", "m", "d", "h", "mi", "s"};
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat datetime(List<Double> rawinputvalue, EpochType epochType, boolean template_reverse) {
        Dat self = new Dat();
        List<Double> value = new ArrayList<>();
        for (int i = 0; i < rawinputvalue.size() && i < Dat.bs_template.length; i++) {
            value.add(rawinputvalue.get(i));
        }
        self.epoch_type = epochType;
        String[] template = template_reverse ? new String[]{"s", "mi", "h", "d", "m", "y"} : new String[]{"y", "m", "d", "h", "mi", "s"};
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat datetime(double[] rawinputvalue, EpochType epochType, boolean template_reverse) {
        Dat self = new Dat();
        List<Double> value = new ArrayList<>();
        for (int i = 0; i < rawinputvalue.length && i < Dat.bs_template.length; i++) {
            value.add(rawinputvalue[i]);
        }
        self.epoch_type = epochType;
        String[] template = template_reverse ? new String[]{"s", "mi", "h", "d", "m", "y"} : new String[]{"y", "m", "d", "h", "mi", "s"};
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat operand(double baserawtime) {

        Dat self = new Dat();
        self.epoch_type = (baserawtime < 0) ? BC : AC;
        List<Double> parts = self.convert_rawtime_to_date(Math.abs(baserawtime));
        self.output = parts;
        self.rawtime = baserawtime;
        return self;
    }

    public static Dat stamp(String rawinput, String rawtemplate, EpochType epochType) {
        Dat self = new Dat();
        List<Double> value = Dat.value_extractor(rawinput);
        String[] template = Dat.template_extractor(rawtemplate);
        self.epoch_type = epochType;
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat stamp(String rawinput, String[] rawtemplate, EpochType epochType) {
        Dat self = new Dat();
        List<Double> value = Dat.value_extractor(rawinput);
        String[] template = Dat.template_extractor(rawtemplate);
        self.epoch_type = epochType;
        self.finalize_full_datetime(value, template);
        return self;
    }

    private static String[] template_extractor(String rawString) {
        
        String[] returnable = new String[bs_template.length];
        Arrays.fill(returnable, null);
        for (String unit : Dat.bs_template) {
            if (rawString.contains(unit)) {
                rawString = rawString.replace(unit, "");
                for(int i = 0; i < returnable.length; i++){
                    if(returnable[i] != null){
                        returnable[i] = unit;
                    }   
                }
            }
        }
        return returnable;
    }

    private static String[] template_extractor(String[] rawString) {
        String[] returnable = new String[bs_template.length];

        int i = 0;
        for (String unit : Dat.bs_template) {
            for (String rwtmp : rawString) {
                if (rwtmp.contains(unit)) {
                    returnable[i] = unit;
                    i+=1;
                    break;
                }
            }
        }
        return returnable;
    }

    private static List<Double> value_extractor(String value) {
        String one_number = "";
        List<Double> several_numbers = new ArrayList<>();
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (INNUMBERS(c)) {
                one_number += c;
            } else {
                if (!one_number.isBlank()) {
                    several_numbers.add(Double.parseDouble(one_number));
                    one_number = "";
                } else {
                    one_number = "";
                }
            }
        }
        if (!one_number.isBlank()) {
            several_numbers.add(Double.parseDouble(one_number));
        }
        return several_numbers;
    }

    private void finalize_full_datetime(List<Double> value, String[] template) {


        String[] template_value_dict = new String[] {"y","m","d","h","mi","s"};

        double[] startresults = new double[template_value_dict.length];
        Arrays.fill(startresults, 0);
        for(int i = 0; i < template.length; i++){
            for(String elm : template_value_dict){
                if (template[i].equals(elm)){
                    try {
                        startresults[i] = value.get(i);
                    } catch (IndexOutOfBoundsException e) {
                        break;
                    }
                }
            }
        }
        
        double total_raw = convert_input_to_rawtime(startresults);



        if (this.epoch_type == BC) { total_raw = -total_raw; }

        this.rawtime = total_raw;

        this.output = convert_rawtime_to_date(total_raw);
    }

    private double convert_input_to_rawtime(double[] template_value_dictionary) {
        try {
            int Y = (int) template_value_dictionary[0];
            int M = (int) template_value_dictionary[1];
            int D = (int) template_value_dictionary[2];
            int h = (int) template_value_dictionary[3];
            int i = (int) template_value_dictionary[4];
            int s = (int) template_value_dictionary[5];





            int threshold_min_clock_value = days_since_epoch(min_clock_value[0],min_clock_value[1],min_clock_value[2]) * 86400;
            int total_days = days_since_epoch(Y, M, D);
            double total = (double) total_days * 86400 + h * 3600 + i * 60 + s - threshold_min_clock_value;
            total = (total < 0) ? 0 : total;  //para evitar que día 0 de un rawtime de 0
            return total;
        } catch (Exception e) {
            e.printStackTrace();
            return -1L;
        }
    }

    private static int days_since_epoch(int Y, int M, int D) {
        int days = 0;
        for (int y : new Range(0, Y, 1)) {
            days += is_leap_year(y) ? 366 : 365;
        }
        for (int m : new Range(1, M, 1)) {
            if (m == 2) {
                days += is_leap_year(Y) ? 29 : 28;
            } else {
                days += mdays[m - 1];
            }
        }
        return days + (D - 1);
    }

    final static int[] mdays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    private List<Double> convert_rawtime_to_date(double seconds) {
        try {
            int days = (int) (seconds / 86400);
            double rem = seconds % 86400;
            int Y = 0;
            while (true) {
                int year_days = is_leap_year(Y) ? 366 : 365;
                if (days >= year_days) {
                    days -= year_days;
                    Y += 1;
                } else break;
            }
            int M = 1;
            while (true) {
                int dim = (M == 2 && is_leap_year(Y)) ? 29 : mdays[M - 1];
                if (days >= dim) {
                    days -= dim;
                    M += 1;
                } else break;
            }
            int D = days + 1;
            int h = (int) (rem / 3600);
            rem %= 3600;
            int i = (int) (rem / 60);
            double s = (double) (rem % 60);

            List <Double> returnable = new ArrayList<>();
            returnable.add((double) Math.max(Y,min_clock_value[0]));
            returnable.add((double) Math.max(M, min_clock_value[1]));
            returnable.add((double) Math.max(D, min_clock_value[2]));
            returnable.add((double) h);
            returnable.add((double) i);
            returnable.add(s);
            return returnable;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private static boolean is_leap_year(int y) {
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }
}


class Dict implements Iterable<Object>{
    private class UnrecognizedKey extends Exception {
        public UnrecognizedKey(String message){super(message);}
    }

    private List<Object> keys;
    private List<Object> values;

    public Dict(List<List<Object>> dataChunk){
        this.keys = new ArrayList<>();
        this.values = new ArrayList<>();
        if(dataChunk!=null){
            for(List<Object> unit: dataChunk){
                if(unit.size()==2) this.add(unit.get(0), unit.get(1));
            }
        }
    }

    @Override
    public Iterator<Object> iterator(){return this.keys.iterator();}

    public void add(List<Object> pair){
        if(pair==null || pair.size()<2) return;
        add(pair.get(0),pair.get(1));
    }

    public void add(Object key,Object value){
        int index = keys.indexOf(key);
        if(index!=-1) values.set(index,value);
        else {keys.add(key); values.add(value);}
    }

    public Object pull(Object key) throws UnrecognizedKey {
        int index = keys.indexOf(key);
        if(index!=-1) return values.get(index);
        throw new UnrecognizedKey("Key not found in Dict: "+key);
    }

    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append("Dict { ");
        for(int i=0;i<keys.size();i++){
            sb.append(keys.get(i)).append("=").append(values.get(i));
            if(i<keys.size()-1) sb.append(", ");
        }
        sb.append(" }");
        return sb.toString();
    }
}
class Range implements Iterable<Integer>{
    private final int start,end,step;

    public Range(int startNumber,int endNumber,int step){
        if(step==0) throw new IllegalArgumentException("Step cannot be zero.");
        this.start=startNumber;
        this.end=endNumber;
        this.step=step;
    }

    @Override
    public Iterator<Integer> iterator(){
        return new Iterator<Integer>(){
            private int current=start;
            @Override public boolean hasNext(){return step>0 ? current<end : current>end;}
            @Override public Integer next(){
                if(!hasNext()) throw new NoSuchElementException();
                int value = current;
                current+=step;
                return value;
            }
        };
    }

    @Override
    public String toString(){return "Range("+start+","+end+")";}
}