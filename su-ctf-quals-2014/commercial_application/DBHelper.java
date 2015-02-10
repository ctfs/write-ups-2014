package edu.sharif.ctf.db;

import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteStatement;
import com.actionbarsherlock.internal.widget.IcsLinearLayout;
import edu.sharif.ctf.R;
import edu.sharif.ctf.config.AppConfig;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class DBHelper extends SQLiteOpenHelper {
    private static String DB_NAME;
    private static String DB_PATH;
    public static final String SELECT_QUERY;
    private static String TABLE_NAME;
    public static final String UPDATE_QUERY;
    private final Context myContext;
    private SQLiteDatabase myDataBase;

    static {
        DB_PATH = "/data/data/edu.sharif.ctf/databases/";
        DB_NAME = "db.db";
        TABLE_NAME = "config";
        UPDATE_QUERY = "UPDATE " + TABLE_NAME + " SET d=?";
        SELECT_QUERY = "SELECT  * FROM " + TABLE_NAME + " WHERE a=1";
    }

    public DBHelper(Context context) {
        super(context, DB_NAME, null, 1);
        this.myContext = context;
    }

    public void createDataBase() throws IOException {
        if (!checkDataBase()) {
            getReadableDatabase();
            try {
                copyDataBase();
            } catch (IOException e) {
                throw new Error("Error copying database");
            }
        }
    }

    private boolean checkDataBase() {
        SQLiteDatabase checkDB = null;
        try {
            checkDB = SQLiteDatabase.openDatabase(DB_PATH + DB_NAME, null, 1);
        } catch (SQLiteException e) {
        }
        if (checkDB != null) {
            checkDB.close();
        }
        return checkDB != null;
    }

    private void copyDataBase() throws IOException {
        InputStream myInput = this.myContext.getAssets().open(DB_NAME);
        OutputStream myOutput = new FileOutputStream(DB_PATH + DB_NAME);
        byte[] buffer = new byte[1024];
        while (true) {
            int length = myInput.read(buffer);
            if (length <= 0) {
                myOutput.flush();
                myOutput.close();
                myInput.close();
                return;
            }
            myOutput.write(buffer, 0, length);
        }
    }

    public void openDataBase() throws SQLException {
        String myPath = DB_PATH + DB_NAME;
        File f = new File(myPath);
        boolean exists = f.exists();
        long length = f.length();
        try {
            this.myDataBase = SQLiteDatabase.openDatabase(myPath, null, R.styleable.SherlockTheme_actionModeShareDrawable);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public synchronized void close() {
        if (this.myDataBase != null) {
            this.myDataBase.close();
        }
        super.close();
    }

    public void onCreate(SQLiteDatabase db) {
    }

    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
    }

    public AppConfig getConfig() {
        boolean z = true;
        AppConfig agency = new AppConfig();
        Cursor cursor = this.myDataBase.rawQuery(SELECT_QUERY, null);
        if (cursor.moveToFirst()) {
            agency.setId(cursor.getInt(0));
            agency.setName(cursor.getString(1));
            agency.setInstallDate(cursor.getString(IcsLinearLayout.SHOW_DIVIDER_MIDDLE)); // 2 == 2014
            if (cursor.getInt(FragmentManagerImpl.ANIM_STYLE_CLOSE_ENTER) <= 0) { // 3 == 0
                z = false;
            }
            agency.setValidLicence(z);
            agency.setSecurityIv(cursor.getString(IcsLinearLayout.SHOW_DIVIDER_END)); // 4 == a5...
            agency.setSecurityKey(cursor.getString(FragmentManagerImpl.ANIM_STYLE_FADE_ENTER)); // 5 == 37eaa...
            agency.setDesc(cursor.getString(R.styleable.SherlockTheme_actionBarSize)); // 7 == ctf.sharif.edu
        }
        return agency;
    }

    public long updateLicence(int licenceCount) {
        SQLiteStatement statement = getWritableDatabase().compileStatement(UPDATE_QUERY);
        statement.bindLong(1, (long) licenceCount);
        return statement.executeInsert();
    }
}
