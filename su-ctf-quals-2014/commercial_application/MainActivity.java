package edu.sharif.ctf.activities;

import android.app.AlertDialog.Builder;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.SimpleOnPageChangeListener;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.Tab;
import com.actionbarsherlock.app.ActionBar.TabListener;
import com.actionbarsherlock.app.SherlockFragment;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.internal.widget.IcsLinearLayout;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuItem;
import com.actionbarsherlock.view.MenuItem.OnActionExpandListener;
import com.actionbarsherlock.widget.ShareActionProvider;
import edu.sharif.ctf.CTFApplication;
import edu.sharif.ctf.R;
import edu.sharif.ctf.adapters.ViewPagerAdapter;
import edu.sharif.ctf.fragments.ListFragment.OnPictureSelectedListener;
import edu.sharif.ctf.security.KeyVerifier;

public class MainActivity extends SherlockFragmentActivity implements OnPictureSelectedListener {
    public static final String NOK_LICENCE_MSG = "Your licence key is incorrect...! Please try again with another.";
    public static final String OK_LICENCE_MSG = "Thank you, Your application has full licence. Enjoy it...!";
    public static boolean isRegisterd;
    private final String CAPTION1;
    private final String CAPTION2;
    private final String CAPTION3;
    private ActionBar actionBar;
    private CTFApplication app;
    FragmentTransaction fragTransactMgr;
    private SimpleOnPageChangeListener onPageChangeListener;
    private TabListener tabListener;
    private ViewPager viewPager;

    class AnonymousClass_4 implements OnClickListener {
        private final /* synthetic */ Context val$context;
        private final /* synthetic */ EditText val$userInput;

        AnonymousClass_4(EditText editText, Context context) {
            this.val$userInput = editText;
            this.val$context = context;
        }

        public void onClick(DialogInterface dialog, int id) {
            if (KeyVerifier.isValidLicenceKey(this.val$userInput.getText().toString(), MainActivity.this.app.getDataHelper().getConfig().getSecurityKey(), MainActivity.this.app.getDataHelper().getConfig().getSecurityIv())) {
                MainActivity.this.app.getDataHelper().updateLicence(2014);
                isRegisterd = true;
                MainActivity.this.showAlertDialog(this.val$context, OK_LICENCE_MSG);
                return;
            }
            MainActivity.this.showAlertDialog(this.val$context, NOK_LICENCE_MSG);
        }
    }

    class AnonymousClass_6 implements View.OnClickListener {
        private final /* synthetic */ Dialog val$dialog;

        AnonymousClass_6(Dialog dialog) {
            this.val$dialog = dialog;
        }

        public void onClick(View v) {
            this.val$dialog.dismiss();
        }
    }

    public MainActivity() {
        this.fragTransactMgr = null;
        this.CAPTION1 = "ListView";
        this.CAPTION2 = "GridView";
        this.CAPTION3 = "ImageView";
        this.onPageChangeListener = new SimpleOnPageChangeListener() {
            public void onPageSelected(int position) {
                super.onPageSelected(position);
                MainActivity.this.actionBar.setSelectedNavigationItem(position);
            }
        };
        this.tabListener = new TabListener() {
            public void onTabSelected(Tab tab, FragmentTransaction ft) {
                MainActivity.this.viewPager.setCurrentItem(tab.getPosition());
            }

            public void onTabUnselected(Tab tab, FragmentTransaction ft) {
            }

            public void onTabReselected(Tab tab, FragmentTransaction ft) {
            }
        };
    }

    static {
        isRegisterd = false;
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.viewPager = (ViewPager) findViewById(R.id.pager);
        this.viewPager.setOnPageChangeListener(this.onPageChangeListener);
        this.viewPager.setAdapter(new ViewPagerAdapter(getSupportFragmentManager()));
        this.fragTransactMgr = getSupportFragmentManager().beginTransaction();
        addActionBarTabs();
        this.app = (CTFApplication) getApplication();
    }

    private void addActionBarTabs() {
        this.actionBar = getSupportActionBar();
        this.actionBar.addTab(this.actionBar.newTab().setIcon((int) R.drawable.ic_4_collections_view_as_list).setTabListener(this.tabListener));
        this.actionBar.addTab(this.actionBar.newTab().setIcon((int) R.drawable.ic_5_content_picture).setTabListener(this.tabListener));
        this.actionBar.setNavigationMode(IcsLinearLayout.SHOW_DIVIDER_MIDDLE);
    }

    public void executeFragment(SherlockFragment fragment) {
        try {
            this.viewPager.removeAllViews();
            this.fragTransactMgr.addToBackStack(null);
            this.fragTransactMgr = getSupportFragmentManager().beginTransaction();
            this.fragTransactMgr.add(this.viewPager.getId(), (Fragment) fragment);
            this.fragTransactMgr.commit();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        getSupportMenuInflater().inflate(R.menu.main, menu);
        ShareActionProvider sap = (ShareActionProvider) menu.findItem(R.id.share).getActionProvider();
        Intent intent = new Intent("android.intent.action.SEND");
        intent.setType("text/plain");
        sap.setShareIntent(intent);
        menu.findItem(R.id.setting).setOnActionExpandListener(new OnActionExpandListener() {
            public boolean onMenuItemActionCollapse(MenuItem item) {
                return true;
            }

            public boolean onMenuItemActionExpand(MenuItem item) {
                return true;
            }
        });
        return true;
    }

    public void onPictureSelected(Integer selectedRow) {
        this.app.setSelectedItem(selectedRow.intValue());
    }

    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() != 2130968634) {
            return super.onOptionsItemSelected(item);
        }
        checkLicenceKey(this);
        return true;
    }

    private void checkLicenceKey(Context context) {
        if (this.app.getDataHelper().getConfig().hasLicence()) {
            showAlertDialog(context, OK_LICENCE_MSG);
            return;
        }
        View promptsView = LayoutInflater.from(context).inflate(R.layout.propmt, null);
        Builder alertDialogBuilder = new Builder(context);
        alertDialogBuilder.setView(promptsView);
        alertDialogBuilder.setCancelable(false).setPositiveButton("Continue", new AnonymousClass_4((EditText) promptsView.findViewById(R.id.editTextDialogUserInput), context)).setNegativeButton("Cancel", new OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                dialog.cancel();
            }
        });
        alertDialogBuilder.create().show();
    }

    private void showAlertDialog(Context context, CharSequence msg) {
        Dialog dialog = new Dialog(context);
        dialog.setContentView(R.layout.dialog);
        dialog.setTitle("CTF 2014");
        ((TextView) dialog.findViewById(R.id.txt)).setText(msg);
        ((Button) dialog.findViewById(R.id.dialogButton)).setOnClickListener(new AnonymousClass_6(dialog));
        dialog.show();
    }
}
