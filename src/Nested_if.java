public class Nestes_if {

    public static void main(String[] args) {
    
    int masuk = 6;
    int jadwal = 6;
    int telat = 7;
    int pulang = 8;

    String tepat = "Anda datang tepat waktu!";
    String terlambat = "Anda datang telat!";
    String terlambat2 = "Ini sudah jadwal pulang!";

    if (masuk == jadwal) {
        System.out.println(tepat);
        if (masuk >= telat) {
            System.out.println(terlambat);
            if (masuk >= pulang) {
                System.out.println(terlambat2);
            }
        }
    }
    }
}
