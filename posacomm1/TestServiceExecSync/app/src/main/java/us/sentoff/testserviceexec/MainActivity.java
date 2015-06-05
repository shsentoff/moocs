package us.sentoff.testserviceexec;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";

    private ServiceConnection mConnection;

    // The Binder that implements Request, obtained when we bind.
    private ICall mICallImpl;

    // A counter to keep track of the requests.
    private int mRequestCount;

    // An ExecutorService to put the calls into the background
    private ExecutorService executor = Executors.newCachedThreadPool();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final int requestCount = mRequestCount++;

                // Run the call synchronously, but on a background thread.
                Runnable runnable = new Runnable() {
                    @Override
                    public void run() {
                        Log.d(TAG, "Making request " + requestCount);
                        int output = 0;
                        // Make the request.
                        try {
                            output = mICallImpl.getStuff(requestCount);
                        } catch (RemoteException e) {
                            e.printStackTrace();
                        }
                        Log.d(TAG, "finished: " + output + " " + Thread.currentThread());
                    }
                };

                executor.execute(runnable);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        Intent intent = new Intent(this, MyService.class);

        // Make the service connection.
        mConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName name, IBinder service) {
                Log.d(TAG, "onServiceConnected");
                mICallImpl = ICall.Stub.asInterface(service);
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                mICallImpl = null;
            }
        };

        bindService(intent, mConnection, BIND_AUTO_CREATE);
    }

    @Override
    protected void onPause() {
        super.onPause();
        unbindService(mConnection);
    }
}
