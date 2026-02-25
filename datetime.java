import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

public class datetime {

    public static void main(String[] args) {
        
        String content = "{0,0,0,0,0,0}";
        Dat a = Dat.datetime(content, Dat.AC,false);
        Dat b = Dat.operand(0);
        System.out.println(a + " " + a.rawtime);
    }
}

class DatMath {

    protected double rawtime;

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

    private static final Dict months = new Dict(Arrays.asList(
            Arrays.asList(1, 2678400), Arrays.asList(2, 2419200), Arrays.asList(3, 2678400),
            Arrays.asList(4, 2592000), Arrays.asList(5, 2678400), Arrays.asList(6, 2592000),
            Arrays.asList(7, 2678400), Arrays.asList(8, 2678400), Arrays.asList(9, 2592000),
            Arrays.asList(10, 2678400), Arrays.asList(11, 2592000), Arrays.asList(12, 2678400)));

    private static final Dict TIME_UNITS = new Dict(Arrays.asList(Arrays.asList("y", 31536000), Arrays.asList("m", months), Arrays.asList("d", 86400), Arrays.asList("h", 3600), Arrays.asList("mi", 60), Arrays.asList("s", 1)));

    private static boolean INNUMBERS(char c) {
        return (c >= '0' && c <= '9') || c == '.';
    }


    protected enum EpochType { AC, BC }
    final static public EpochType AC = EpochType.AC;
    final static public EpochType BC = EpochType.BC;

    private enum DataType { fulldat }
    final static public DataType fulldat = DataType.fulldat;

    private static final String[] bs_template = {"y", "m", "d", "h", "mi", "s"};

    int converter;
    int[] min_clock_value = new int[3];

    public DataType source = fulldat;
    public List<Float> output = new ArrayList<>();
    public EpochType epoch_type;

    public Dat() {
        super();
        Arrays.fill(min_clock_value, 1);
    }

    class TooManyValuesException extends Exception {
        public TooManyValuesException(String msg) {
            super(msg);
        }
    }

    class TooManyParametersException extends Exception {
        public TooManyParametersException(String msg) {
            super(msg);
        }
    }

    @Override
    public String toString() {
        int Y = this.output.get(0).intValue();
        int M = this.output.get(1).intValue();
        int D = this.output.get(2).intValue();
        int h = this.output.get(3).intValue();
        int mi = this.output.get(4).intValue();
        int s = Math.round(this.output.get(5));

        String epochType = (this.rawtime < 0) ? BC.name() : AC.name();

        if (this.source == fulldat) {
            return String.format("(%04d-%02d-%02d %02d:%02d:%02d)%s", Y, M, D, h, mi, s, epochType);
        } else {
            return "Huuuuuuge errrorrr, idk what happeneeeneeddddd, error 404";
        }
    }

    public static Dat datetime(String rawinputvalue, EpochType epochType, boolean template_reverse) {
        Dat self = new Dat();
        List<Float> value = self.value_extractor(rawinputvalue);
        self.epoch_type = epochType;
        String[] template = template_reverse ? new String[]{"s", "mi", "h", "d", "m", "y"} : new String[]{"y", "m", "d", "h", "mi", "s"};
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat datetime(List<Number> rawinputvalue, EpochType epochType, boolean template_reverse) {
        Dat self = new Dat();
        List<Float> value = new ArrayList<>();
        for (int i = 0; i < rawinputvalue.size() && i < Dat.bs_template.length; i++) {
            value.add(rawinputvalue.get(i).floatValue());
        }
        self.epoch_type = epochType;
        String[] template = template_reverse ? new String[]{"s", "mi", "h", "d", "m", "y"} : new String[]{"y", "m", "d", "h", "mi", "s"};
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat operand(double baserawtime) {
        Dat self = new Dat();
        self.epoch_type = (baserawtime < 0) ? BC : AC;
        List<Float> parts = self.convert_rawtime_to_date(Math.abs(baserawtime));
        self.output = parts;
        return self;
    }

    public static Dat stamp(String rawinput, String rawtemplate, EpochType epochType) {
        Dat self = new Dat();
        List<Float> value = self.value_extractor(rawinput);
        String[] template = self.template_extractor(rawtemplate);
        self.epoch_type = epochType;
        self.finalize_full_datetime(value, template);
        return self;
    }

    public static Dat stamp(String rawinput, String[] rawtemplate, EpochType epochType) {
        Dat self = new Dat();
        List<Float> value = self.value_extractor(rawinput);
        String[] template = self.template_extractor(rawtemplate);
        self.epoch_type = epochType;
        self.finalize_full_datetime(value, template);
        return self;
    }

    private String[] template_extractor(String rawString) {
        
        List<String> returnable = new ArrayList<>();
        for (String unit : Dat.bs_template) {
            if (rawString.contains(unit)) {
                rawString = rawString.replace(unit, "");
                returnable.add(unit);
            }
        }
        return returnable.toArray(new String[0]);
    }

    private String[] template_extractor(String[] rawString) {
        List<String> returnable = new ArrayList<>();
        for (String unit : Dat.bs_template) {
            for (String rwtmp : rawString) {
                if (rwtmp.contains(unit)) {
                    returnable.add(unit);
                    break;
                }
            }
        }
        return returnable.toArray(new String[0]);
    }

    private List<Float> value_extractor(String value) {
        String one_number = "";
        List<Float> several_numbers = new ArrayList<>();
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (INNUMBERS(c)) {
                one_number += c;
            } else {
                if (!one_number.isBlank()) {
                    several_numbers.add(Float.parseFloat(one_number));
                    one_number = "";
                } else {
                    one_number = "";
                }
            }
        }
        if (!one_number.isBlank()) {
            several_numbers.add(Float.parseFloat(one_number));
        }
        return several_numbers;
    }

    private void finalize_full_datetime(List<Float> value, String[] template) {
        Dict template_value_dictionary = new Dict(Arrays.asList(
                Arrays.asList("y", 0), Arrays.asList("m", 1), Arrays.asList("d", 1),
                Arrays.asList("h", 0), Arrays.asList("mi", 0), Arrays.asList("s", 0)
        ));

        for (int i = 0; i < template.length; i++) {
            for (Object key : template_value_dictionary) {
                if (template[i].equals(key)) {
                    try {
                        template_value_dictionary.add(key, value.get(i));
                        break;
                    } catch (IndexOutOfBoundsException e) {
                        break;
                    }
                }
            }
        }

        double total_raw = convert_input_to_rawtime(template_value_dictionary);
        if (this.epoch_type == BC) { total_raw = -total_raw; }
        this.rawtime = total_raw;
        this.output = convert_rawtime_to_date(total_raw);
    }

    private double convert_input_to_rawtime(Dict template_value_dictionary) {
        try {
            int Y = ((Number) template_value_dictionary.pull("y")).intValue();
            int M = ((Number) template_value_dictionary.pull("m")).intValue();
            int D = ((Number) template_value_dictionary.pull("d")).intValue();
            int h = ((Number) template_value_dictionary.pull("h")).intValue();
            int i = ((Number) template_value_dictionary.pull("mi")).intValue();
            int s = ((Number) template_value_dictionary.pull("s")).intValue();

            int total_days = days_since_epoch(Y, M, D);
            double total = (double) total_days * 86400 + h * 3600 + i * 60 + s;
            if (total < 0)  //para evitar que día 0 de un rawtime de 0
                total = 0;
            return total;
        } catch (Exception e) {
            e.printStackTrace();
            return -1L;
        }
    }

    private int days_since_epoch(int Y, int M, int D) {
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

    final int[] mdays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    private List<Float> convert_rawtime_to_date(double seconds) {
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
            float s = (float) (rem % 60);

            List<Float> returnable = new ArrayList<>();
            returnable.add((float) Math.max(Y,min_clock_value[0]));
            returnable.add((float) Math.max(M, min_clock_value[1]));
            returnable.add((float) Math.max(D, min_clock_value[2]));
            returnable.add((float) h);
            returnable.add((float) i);
            returnable.add(s);
            return returnable;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private boolean is_leap_year(int y) {
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }

}

/**
 * biggest Pythonist heist since the times of Mickel Jackson
 */
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