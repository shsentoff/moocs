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


public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";

    private ServiceConnection mConnection;

    // The Binder that implements Request, obtained when we bind.
    private IRequest mIRequestImpl;

    // A counter to keep track of the requests.
    private int mRequestCount;

    // Create the stub for handling the reply.
    // This is sent with a request, so the service can call back.
    private final IReply.Stub mIReplyImpl = new IReply.Stub() {
        @Override
        public void started(int input) throws RemoteException {
            Log.d(TAG, "started: " + input + " " + Thread.currentThread());
        }

        @Override
        public void finished(int output) throws RemoteException {
            Log.d(TAG, "finished: " + output + " " + Thread.currentThread());
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int requestCount = mRequestCount++;

                Log.d(TAG, "Making request " + requestCount);
                // Make the request.
                try {
                    mIRequestImpl.getStuff(requestCount, mIReplyImpl);
                } catch (RemoteException e) {
                    e.printStackTrace();
                }

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
                mIRequestImpl = IRequest.Stub.asInterface(service);
            }

            @Override
            public void onServiceDisconnected(ComponentName name) {
                mIRequestImpl = null;
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
