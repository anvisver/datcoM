
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class datetime {
    
    
    public static void main(String[] args) {
    // 1. Creamos el diccionario con valores iniciales
    // Usamos la estructura de lista de listas que acepta tu constructor
    String content = "{1,2,3,4,5,6}";
    dat a = new dat();
    a.datetime(content, false );
    } 
        
}




class dat {

    private static final Dict months = new Dict(Arrays.asList(
            Arrays.asList(1, 2678400), Arrays.asList(2, 2419200), Arrays.asList(3, 2678400),
            Arrays.asList(4, 2592000), Arrays.asList(5, 2678400), Arrays.asList(6, 2592000),
            Arrays.asList(7, 2678400), Arrays.asList(8, 2678400), Arrays.asList(9, 2592000),
            Arrays.asList(10, 2678400), Arrays.asList(11, 2592000), Arrays.asList(12, 2678400)
        ));
    private static final Dict TIME_UNITS = new Dict(Arrays.asList(
            Arrays.asList("y", 31536000), 
            Arrays.asList("m", months), 
            Arrays.asList("d", 86400),
            Arrays.asList("h", 3600), 
            Arrays.asList("mi", 60), 
            Arrays.asList("s", 1)
    ));

    private static final boolean INNUMBERS(String character) {
            /*befiefnefe */
            // Added 0 to the list
            final int[] NUMBERS = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
            
            try {
                int parsed = Integer.parseInt(character);
                for (int i = 0; i < NUMBERS.length; i++) {
                    if (parsed == NUMBERS[i]) {
                        return true;
                    }
                }
            } catch (NumberFormatException e) {
                // If it's not a number at all (like "A"), return false
                return false;
            }
            return false;
        }
    public boolean checkAllTypes(Object rawlist, Class<?> targetClass) {
        if(rawlist instanceof List list){
        
        for (Object obj : list) {
            // If even one element doesn't match the class, return false immediately
            if (!targetClass.isInstance(obj)) {
                return false;}
        }
        return true;}return false;
    }
    private static enum EpochType {AC , BC}

    final static public EpochType AC = EpochType.AC;
    final static public EpochType BC = EpochType.BC;

    private static enum DataType {fulldat}

    final static public DataType fulldat = DataType.fulldat;


    private  static final String[] bs_template = {"y", "m", "d", "h", "mi", "s"};

    float rawtime; 
    int converter; 
    int[] min_clock_value = new int[3];

    public DataType source;
    public List < Float > output = new ArrayList<>();
    public EpochType epoch_type;

    public dat(){

        Arrays.fill(min_clock_value, 1);
        source = fulldat;

    }
    
    public void datetime(Object rawinputvalue, boolean template_reverse) {
        
        this.min_clock_value = new int[] {1,1,1};
        List<Float> value = new ArrayList<>();

        if(rawinputvalue instanceof String input_value){
        value = this.value_template_extractor(input_value);}
        else{//got to work here...}
        String[] template = new String[bs_template.length];

        if(template_reverse){
            for (int i = 0; i < bs_template.length; i++) {
                // Take from the end of 'original', place at the start of 'reversed'
                template[i] = bs_template[bs_template.length - 1 - i];}
        }
        else{
            template = bs_template;}
        
        //still needing to make finalize datetime for this shit to work
        System.out.println(this.finalize_full_datetime(value,template, AC, fulldat));}}

    




    private List<Float> value_template_extractor(String value){

        String one_number = "";
        List<Float> several_numbers = new ArrayList<>();
        for(int i = 0; i < value.length(); i++){
            if(INNUMBERS(value.substring(i))){
                one_number += value;
            }
            else{
                if(one_number.strip().length() != 0){
                    several_numbers.add(Float.parseFloat(one_number));
                    one_number = "";
                }
            }


        }

        if(one_number.length() > 0){

            boolean found = true;
            for(int i = 0; i < one_number.length(); i++){
                if(!INNUMBERS(one_number.substring(i))){
                    found = false;
                }
            }
            if (found){
                several_numbers.add(Float.parseFloat(one_number));
            }}
        return several_numbers;
    }   
        //else if (!(rawvalue instanceof List && (checkAllTypes(rawvalue, Float.class) || checkAllTypes(rawvalue, Integer.class)) )){//detect value if not list[float | int]
        //raise value error
    private Object finalize_full_datetime(List<Float> value,String[]template, EpochType epoch_type, DataType output_type){

        Dict template_value_dictionary = new Dict(Arrays.asList(Arrays.asList("y", 0),Arrays.asList("m", 1),Arrays.asList("d", 1),Arrays.asList("h", 0),Arrays.asList("mi", 0),Arrays.asList("s", 0)));

        for(int i = 0; i < template.length; i++){
            for(Object key : template_value_dictionary){
                if(template[i] == key){
                    try {
                        template_value_dictionary.add(key, value.get(i));
                        break;
                    } catch (IndexOutOfBoundsException e) {
                        break;
                        // TODO: handle exception
                    }
                }
            }}

        template_value_dictionary = normallize_full(template_value_dictionary);
        float total_raw = convert_input_to_rawtime(template_value_dictionary);
        if(epoch_type == BC){total_raw = -total_raw;}

        this.rawtime = total_raw;

        this.output = convert_rawtime_to_date(total_raw);

        this.source = output_type;

        return this; 
    }
    @Override
    public String toString(){

        int Y = this.output.get(0).intValue();
        int M = this.output.get(1).intValue();
        int D = this.output.get(2).intValue();
        int h = this.output.get(3).intValue();
        int mi = this.output.get(4).intValue();
        int s = this.output.get(5).intValue();

        String epochType;
        if (this.rawtime < 0){
        epochType = AC.name();}
        else{epochType = BC.name();}




        if(this.source == fulldat){
            return String.format("(%04d-%02d-%02d %02d:%02d:%02d)%s",
                             Y, M, D, h, mi, s, epochType);
                            
        }
        else{return "abc";}


    }
    private float convert_input_to_rawtime(Dict template_value_diccionary){try {
        

        Dict vals = template_value_diccionary;

        int Y = (int) vals.pull("y");
        int M = (int) vals.pull("m");
        int D = (int) vals.pull("d");
        int h = (int) vals.pull("h");
        int i = (int) vals.pull("mi");
        int s = (int) vals.pull("s");

        int total_days = days_since_epoch(Y, M, D);
        float total = total_days * 86400 + h * 3600 + i * 60 + (float) s;


        return total;
    } catch (Exception e) {
        e.printStackTrace();
        return -1;
        
        // TODO: handle exception
    }}
    private int days_since_epoch(int Y, int M, int D){

        int[] mdays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        int days = 0;

        for(int y : new Range(1,M,1)){

            days += is_leap_year(y) ? 366 : 365;
        }

        for(int m : new Range(1,M,1)){
            
            if (m == 2) {
                days += is_leap_year(Y) ? 29 : 28;
            } else {
                days += mdays[m - 1];
            }
        }
        return days + (D - 1);
    }
    private List <Float> convert_rawtime_to_date(float seconds){
        try{
        int days = (int) (seconds / (int) TIME_UNITS.pull("d"));
        float rem = seconds % (int) TIME_UNITS.pull("d");
        int Y = 0;

        while(true){

            int year_days = is_leap_year(Y) ? 366 : 365;
            if(days >= year_days){
                days -= year_days;
            }
            else{
                break;}

        }

        int[] mdays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

        int M = 1;
        while(true){
            int dim;
            if ( M == 2 && is_leap_year(Y)){
                dim = 29;
            }
            else{dim = mdays[M - 1];}

            if( days >= dim){
                days -= dim;
                M += 1;

            }
            else{
                break;}
            
        }
        int D = days + 1;
        int h = (int) rem / (int) TIME_UNITS.pull("h");
        rem %= (int)TIME_UNITS.pull("h");
        int i = ((int) rem / 60);
        float s = rem / 60;

        List < Float > returnable = new ArrayList<>();

        returnable.add((float) Y);
        returnable.add((float) M);
        returnable.add((float) D);
        returnable.add((float) h);
        returnable.add((float) i);
        returnable.add(s);



        return returnable;
    
    }
        catch(Exception e){
            e.printStackTrace();
            return null;
        }
    }

    private boolean is_leap_year(int y){
        return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    }
    private int days_in_month(int year, int month) {
        // Instancia en una sola línea
        Dict month_day_converter = new Dict(Arrays.asList(Arrays.asList(1, 31), Arrays.asList(2, 28), Arrays.asList(3, 31), Arrays.asList(4, 30), Arrays.asList(5, 31), Arrays.asList(6, 30), Arrays.asList(7, 31), Arrays.asList(8, 31), Arrays.asList(9, 30), Arrays.asList(10, 31), Arrays.asList(11, 30), Arrays.asList(12, 31)));

        if (month == 2) {
            return is_leap_year(year) ? 29 : 28;
        }

        try {
            // Usamos 'month' directamente porque las llaves del dict son 1, 2, 3...
            return (int) month_day_converter.pull(month);
        } catch (Exception e) {
            return 0; 
        }
    }
    private int days_in_year(int year){if(is_leap_year(year)){return 366;}else{return 365;} }
    private Dict normallize_full(Dict template_value_dictionary) {
    try {
        // Extraer valores del Dict
        float Yf = (float) template_value_dictionary.pull("y");
        float Mf = (float) template_value_dictionary.pull("m");
        float Df = (float) template_value_dictionary.pull("d");
        float hf = (float) template_value_dictionary.pull("h");
        float mif = (float) template_value_dictionary.pull("mi");
        float sf = (float) template_value_dictionary.pull("s");

        // Normalización inicial de tiempo a días
        mif += (int) (sf / 60);
        sf = sf % 60;

        hf += (int) (mif / 60);
        mif = mif % 60;

        Df += (int) (hf / 24); // Sumamos a Df, no lo sobrescribimos
        hf = hf % 24;

        // Manejo de años fraccionarios
        int Y_int = (int) Yf;
        float fracY = Yf - Y_int;
        if (fracY != 0) {
            Df += fracY * days_in_year(Y_int);
        }
        int Y = Y_int;

        // Manejo de meses fraccionarios
        int M_int = (int) Mf;
        float fracM = Mf - M_int;

        if (M_int <= 0) { M_int = 1; }
        int years_from_months = (M_int - 1) / 12;
        int M = (M_int - 1) % 12;
        M += 1;
        Y += years_from_months;

        if (fracM != 0.0f) {
            Df += fracM * days_in_month(Y, M);
        }

        // Convertir Df acumulado a días enteros y fracción
        int day = (int) Df;
        float D_frac = Df - day;

        // Primer bucle de normalización de calendario (ajuste de desbordamiento de días)
        while (true) {
            int dim = days_in_month(Y, M);
            if (day < 1) {
                M -= 1;
                if (M < 1) { M = 12; Y -= 1; }
                day += days_in_month(Y, M);
            } else if (day > dim) {
                day -= dim;
                M += 1;
                if (M > 12) { M = 1; Y += 1; }
            } else {
                break;
            }
        }

        // Procesar la fracción de día restante hacia horas, minutos y segundos
        hf += D_frac * 24.0;
        int h_int = (int) hf;
        double hf_frac = hf - h_int;

        mif = (float) (hf_frac * 60.0);
        int mi_int = (int) mif;
        double mif_frac = mif - mi_int;

        sf = (float) (mif_frac * 60.0);

        // Normalización final (por si las fracciones generaron desbordamientos)
        mi_int += (int) (sf / 60);
        sf = sf % 60;
        h_int += (int) (mi_int / 60);
        mi_int = mi_int % 60;
        day += (int) (h_int / 24);
        h_int = h_int % 24;

        // Segundo bucle de normalización (ajuste final de calendario)
        while (true) {
            int dim = days_in_month(Y, M);
            if (day < 1) {
                M -= 1;
                if (M < 1) { M = 12; Y -= 1; }
                day += days_in_month(Y, M);
            } else if (day > dim) {
                day -= dim;
                M += 1;
                if (M > 12) { M = 1; Y += 1; }
            } else {
                break;
            }
        }

        // Construir el Dict de resultado
        Dict result = new Dict(null); // Usamos el constructor vacío

        int finalY = (Y >= min_clock_value[0]) ? Y : 1; //a la derecha el "if", a la izquierda el "else"
        int finalM = (M >= min_clock_value[1]) ? M : 1;
        int finalDay = (day >= min_clock_value[2]) ? day : 1;

        result.add("y", finalY);
        result.add("m", finalM);
        result.add("d", finalDay);
        result.add("h", h_int);
        result.add("mi", mi_int);
        result.add("s", sf);

        return result;

    } catch (Exception e) {
        e.printStackTrace();
        return null; 
    }

}
}




class Dict implements Iterable<Object> {
    private class UnrecognizedKey extends Exception {
        public UnrecognizedKey(String message) {
            super(message);
        }
    }

    private List<Object> keys;
    private List<Object> values;

    public Dict(List<List<Object>> dataChunk) {
        this.keys = new ArrayList<>();
        this.values = new ArrayList<>();

        if (dataChunk != null) {
            for (List<Object> unit : dataChunk) {
                if (unit.size() == 2) {
                    this.add(unit.get(0), unit.get(1));
                }
            }
        }
    }

    @Override
    public Iterator<Object> iterator() {
        return this.keys.iterator();
    }

    public void add(List<Object> pair) {
        if (pair == null || pair.size() < 2) return;
        add(pair.get(0), pair.get(1));
    }

    public void add(Object key, Object value) {
        int index = keys.indexOf(key); // Buscamos si ya existe

        if (index != -1) {
            // Si existe, actualizamos el valor en ese índice
            values.set(index, value);
        } else {
            // Si no existe, añadimos
            keys.add(key);
            values.add(value);
        }
    }

    public Object pull(Object key) throws UnrecognizedKey {
        int index = keys.indexOf(key);
        if (index != -1) {
            return values.get(index);
        }
        throw new UnrecognizedKey("Key not found in Dict: " + key);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Dict { ");
        for (int i = 0; i < keys.size(); i++) {
            sb.append(keys.get(i)).append("=").append(values.get(i));
            if (i < keys.size() - 1) sb.append(", ");
        }
        sb.append(" }");
        return sb.toString();

        
    }
}

class Range implements Iterable<Integer> {


    private final int start;
    private final int end;
    private final int step;

    public Range(int startNumber, int endNumber, int step) {
        if (step == 0) {
            throw new IllegalArgumentException("Step cannot be zero.");
        }

        this.start = startNumber;
        this.end = endNumber;
        this.step = step;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<Integer>() {

            private int current = start;

            @Override
            public boolean hasNext() {
                if (step > 0) {
                    return current < end;
                } else {
                    return current > end;
                }
            }

            @Override
            public Integer next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }

                int value = current;
                current += step;
                return value;
            }
        };
    }

    @Override
    public String toString() {
        return "Range(" + start + ", " + end + ")";
    }
}


