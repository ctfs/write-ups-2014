import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class keym {
	public static final String CIPHER_ALGORITHM = "AES/CBC/PKCS5Padding";
	public static final String VALID_LICENCE = "29a002d9340fc4bd54492f327269f3e051619b889dc8da723e135ce486965d84";
	public static final String SECRET_KEY = "37eaae0141f1a3adf8a1dee655853714";
	public static final String SECRET_IV = "a5efdbd57b84ca36";

	public static boolean isValidLicenceKey(String userInput, String secretKey, String iv) {
		return encrypt(userInput, secretKey, iv).equals(VALID_LICENCE);
	}

	public static String encrypt(String userInput, String secretKey, String iv) {
		String encryptedText = "";
		try {
			SecretKeySpec secretKeySpec = new SecretKeySpec(hexStringToBytes(secretKey), "AES");
			Cipher cipher = Cipher.getInstance(CIPHER_ALGORITHM);
			cipher.init(1, secretKeySpec, new IvParameterSpec(iv.getBytes()));
			encryptedText = bytesToHexString(cipher.doFinal(userInput.getBytes()));
		} catch (Exception e) {
			e.printStackTrace();
		}
		return encryptedText;
	}

	public static String decrypt(String userInput, String secretKey, String iv) {
		String encryptedText = "";
		try {
			SecretKeySpec secretKeySpec = new SecretKeySpec(hexStringToBytes(secretKey), "AES");
			Cipher cipher = Cipher.getInstance(CIPHER_ALGORITHM);
			cipher.init(2, secretKeySpec, new IvParameterSpec(iv.getBytes()));
			encryptedText = bytesToHexString(cipher.doFinal(hexStringToBytes(userInput)));
		} catch (Exception e) {
			e.printStackTrace();
		}
		return encryptedText;
	}

	public static String bytesToHexString(byte[] bytes) {
		StringBuilder sb = new StringBuilder();
		int length = bytes.length;
		for (int i = 0; i < length; i++) {
			sb.append(String.format("%02x", new Object[]{Integer.valueOf(bytes[i] & 255)}));
		}
		return sb.toString();
	}

	public static byte[] hexStringToBytes(String s) {
		int len = s.length();
		byte[] data = new byte[(len / 2)];
		for (int i = 0; i < len; i += 2) {
			data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4) + Character.digit(s.charAt(i + 1), 16));
		}
		return data;
	}

	public static void main(String[] args) {
		System.out.println(decrypt(VALID_LICENCE, SECRET_KEY, SECRET_IV));
	}
}
