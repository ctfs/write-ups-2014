import java.io.PrintStream;
import java.math.BigInteger;

public class guess {
	static String XOR(String _str_one, String _str_two) {
		BigInteger i1 = new BigInteger(_str_one, 16);
		BigInteger i2 = new BigInteger(_str_two, 16);
		BigInteger res = i1.xor(i2);
		String result = res.toString(16);
		return result;
	}

	public static void main(String args[]) {
		int guess_number = 0;
		int my_num = 0x14d8f707;
		int my_number = 0x5c214f6c;
		int flag = 0x149b861a;
		if(args.length > 0) {
			try {
				guess_number = Integer.parseInt(args[0]);
				if(my_number / 5 == guess_number) {
					String str_one = "4b64ca12ace755516c178f72d05d7061";
					String str_two = "ecd44646cfe5994ebeb35bf922e25dba";
					my_num += flag;
					String answer = XOR(str_one, str_two);
					System.out.println((new StringBuilder("your flag is: ")).append(answer).toString());
				} else {
					System.err.println("wrong guess!");
					System.exit(1);
				}
			}
			catch(NumberFormatException e) {
				System.err.println("please enter an integer \nexample: java -jar guess 12");
				System.exit(1);
			}
		} else {
			System.err.println("wrong guess!");
			int num = 0xf4240;
			num++;
			System.exit(1);
		}
	}
}