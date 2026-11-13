import java.util.Scanner;

class chall {
   public static String fourth(String var0) {
      String var10000 = var0.substring(19);
      return var10000 + var0.substring(0, 19);
   }

   public static String third(String var0) {
      String var1 = "";

      for(int var2 = 0; var2 < var0.length(); ++var2) {
         if (var2 % 3 == 0) {
            var1 = var1 + (char)(var0.charAt(var2) + var2 / 3);
         } else if (var2 % 3 == 2) {
            var1 = var1 + (char)(var0.charAt(var2) + (var2 - 2) / 3);
         } else {
            var1 = var1 + var0.charAt(var2);
         }
      }

      return var1;
   }

   public static String second(String var0) {
      String var1 = var0.substring(0, 2);
      String var2 = var0.substring(2, var0.length() - 16);
      String var3 = var0.substring(var0.length() - 16);
      return var3 + var2 + var1;
   }

   public static String first(String var0) {
      int[] var1 = new int[]{-16, 13, -18, -20, 15, -3, 6, -1, -15, 11, -11, -17, -15, -16, 3, -3, 4, -11, 19, 20, -10, 11, 9, 2, -12, -14, -3, 0, 0, 13, 12, -12, -18, 18, 6, -6, 4, 5, 3, -6, -15, -3, -5, -3, 10, 0};
      String var2 = "";

      for(int var3 = 0; var3 < var0.length(); ++var3) {
         var2 = var2 + (char)(var0.charAt(var3) + var1[var3]);
      }

      return var2;
   }

   public static void main(String[] var0) {
      Scanner var1 = new Scanner(System.in);
      String var2 = var1.nextLine();
      String var3 = "?PsaC~F^oKk/qcBzeWKw(<lg-'9b9EB1UGq9iro+vHFYq_";
      if (var2.length() == 46 && first(second(third(fourth(var2)))).equals(var3)) {
         System.out.println("Congratulations!!!!!!!!, Access Granted");
      } else {
         System.out.println("Access Denied! Please try again!");
      }

      var1.close();
   }
}
