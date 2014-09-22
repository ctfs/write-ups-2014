import java.io.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Files;
import java.util.HashMap;

/**
 * Created by Controllerface on 9/19/2014.
 *
 * A Java implementation of a "CSAWlz" format decompressor. This was written after the CTF was over
 * using the challenge author's C++ code as a reference for the hashing/decompressing algorithm.
 * This example assumes you have the file "weissman.csawlz" inside a "csaw2014" subdirectory, which
 * is itself inside your home directory (which will vary depending on platform).
 *
 * After running, the files inside the challenge archive will be extracted to the same directory
 * that the archive was read from.
 */
public class CSAWlz {

    public static void main(String args[]) throws Exception
    {
        String homedir = System.getProperty("user.home");

        // read the file from disk
        FileInputStream data = new FileInputStream(homedir+"/csaw2014/weissman.csawlz");

        // create input buffered stream to hold the raw bytes
        BufferedInputStream bufferedInput = new BufferedInputStream(data, 1024);

        System.out.println("\nHeader Data:\n-----------");

        // read the magic number (which doesn't really matter at all)
        byte magic[] = readData(bufferedInput,8);
        System.out.println(" Magic Bytes: " + new String(magic));

        // read the version number (which also doesn't matter)
        byte versionData[] = readData(bufferedInput,4);
        int version = ByteBuffer.wrap(versionData).order(ByteOrder.LITTLE_ENDIAN).getInt();
        System.out.println(" Version:     " + version);

        // read the number of files stored in the archive
        byte fileCountData[] = readData(bufferedInput,4);
        int fileCount = ByteBuffer.wrap(fileCountData).order(ByteOrder.LITTLE_ENDIAN).getInt();
        System.out.println(" File Count:  " + fileCount);

        extract(bufferedInput,fileCount,homedir+"/csaw2014/");
    }

    /**
     * Just a simple utility method to read n bytes from an input stream
     * @param in the input stream to read from
     * @param size the amount of bytes to read
     * @return a byte array containing the bytes read
     * @throws Exception
     */
    private static byte[] readData(InputStream in, int size) throws Exception
    {
        byte value[] = new byte[size];
        in.read(value,0,size);
        return value;
    }

    /**
     * This is the actual hashing algorithm the author used, but converted from
     * C++ to Java. This is of course what people were expected to "guess" along
     * with all the other things about control bytes, sizes, offsets, etc. in
     * order to extract the compressed files.
     *
     * @param bytesToHash the bytes to generate a hash for. only the first 4 are used
     * @return a 16 bit numeric hash of the input
     */
    private static short doHash(byte bytesToHash[])
    {
        int hash = 0x55aa55aa;
        hash ^= ((hash << 5) + bytesToHash[0] + (hash >>> 2));
        hash ^= ((hash << 5) + bytesToHash[1] + (hash >>> 2));
        hash ^= ((hash << 5) + bytesToHash[2] + (hash >>> 2));
        hash ^= ((hash << 5) + bytesToHash[3] + (hash >>> 2));
        return (short)hash;
    }

    /**
     * Extracts all files from the "CSAWlz" format archive stored in the input stream.
     *
     * @param input the CSAWlz file input
     * @param fileCount the number of files present in the archive
     * @param outputDirectory  the directory to write the files to
     * @throws Exception
     */
    private static void extract(InputStream input, int fileCount, String outputDirectory) throws Exception
    {
        for (int i =0; i<fileCount;i++) {
            System.out.println("\nFile " +(i+1)+ ":\n-----------");
            byte magic_1[] = readData(input, 4);
            int magic1_int = ByteBuffer.wrap(magic_1).order(ByteOrder.LITTLE_ENDIAN).getInt();
            System.out.println(" Magic Number      : " + magic1_int);
            byte csize_1[] = readData(input, 4);
            int csize1_int = ByteBuffer.wrap(csize_1).order(ByteOrder.LITTLE_ENDIAN).getInt();
            System.out.println(" Compressed Size   : " + csize1_int);
            byte usize_1[] = readData(input, 4);
            int usize1_int = ByteBuffer.wrap(usize_1).order(ByteOrder.LITTLE_ENDIAN).getInt();
            System.out.println(" Uncompressed Size : " + usize1_int);
            byte fname_1[] = readData(input, 32);
            String fileName = new String(fname_1).trim();
            System.out.println(" File Name         : " + fileName);
            byte fdata_1[] = readData(input, csize1_int);
            File outputFile = new File(outputDirectory+fileName);
            Files.createFile(outputFile.toPath());
            OutputStream outputStream = new FileOutputStream(outputDirectory + fileName,true);
            ByteArrayOutputStream file = new ByteArrayOutputStream(fdata_1.length);
            decompress(file, fdata_1);
            file.writeTo(outputStream);
            outputStream.close();
        }
    }

    /**
     * Decompress a single file and store the decompressed bytes in the file object
     * that is passed in. The data array holds the raw, compressed bytes to decompress.
     *
     * @param file output stream to write decompressed bytes to
     * @param data input data to decompress
     * @throws Exception
     */
    private static void decompress(ByteArrayOutputStream file, byte[] data) throws Exception
    {
        HashMap<Short,byte[]> runs = new HashMap<>();
        int currentPosition = 0;
        boolean go = true;
        while (go)
        {
            byte currentControl = data[currentPosition];
            int size = currentControl >> 1;
            boolean isCompressed = (currentControl & 0b00000001) != 0b00000001;
            if (isCompressed)
            {
                /*
                 This is how you fake it, which is what everyone did during the challenge
                  */
                //byte padding[] = new byte[size];
                //file.write(padding);

                /*
                 THIS is how you ACTUALLY decompress the data
                  */
                // create an array to hold the stored hash and copy the
                // hash bytes from the data stream
                byte hashBytes[] = new byte[2];
                System.arraycopy(data,currentPosition+1,hashBytes,0,2);
                // convert the stored bytes into a short, which is how the
                // hash is stored
                short hash = ByteBuffer.wrap(hashBytes).order(ByteOrder.LITTLE_ENDIAN).getShort();
                // create an array to hold the decompressed bytes and copy
                // them from the hash table
                byte decompressedBytes[] = new byte[size];
                System.arraycopy(runs.get(hash), 0, decompressedBytes, 0, size);
                // write the decompressed bytes to the output stream, and
                // advance the position index to the next control byte
                file.write(decompressedBytes);
                currentPosition = currentPosition + 3;
            }
            else
            {
                // since this isn't a compressed block, we just need to copy
                // the appropriate bytes from the input to the output
                byte bytesToWrite[] = new byte[size];
                System.arraycopy(data, currentPosition+1, bytesToWrite, 0, size);

                /*
                THIS is the part that allows the REAL decompressing algorithm to work
                 */
                // using the same hashing algorithm that the author used to
                // generate hashes when compressing, generate a matching hash
                short hash = doHash(bytesToWrite);
                // now using that hash, store it and the accompanying bytes in a hash
                // table so they can be used later for decompressing
                runs.put(hash,bytesToWrite);
                // now write the bytes directly to the output and advance the
                // position index to the next control byte
                file.write(bytesToWrite);
                currentPosition = currentPosition+1+size;
            }
            if (currentPosition > data.length-1)
                go = false;
        }
    }
}
