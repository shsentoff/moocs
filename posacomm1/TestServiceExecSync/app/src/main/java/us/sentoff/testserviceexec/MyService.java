package us.sentoff.testserviceexec;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;

public class MyService extends Service {
    private final static String TAG = "MyService";

    public MyService() {
    }

    // Create the stub for handling the request.
    // This is sent from onBind, so that the proxy can send us requests.
    private final ICall.Stub mICallImpl = new ICall.Stub() {
        @Override
        public int getStuff(final int input) throws RemoteException {
            Log.d(TAG, "started: " + Thread.currentThread());

            // Wait
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            Log.d(TAG, "finished: " + Thread.currentThread());

            return input + 1000;
        }
    };

    @Override
    public IBinder onBind(Intent intent) {
        // Return the communication channel to the service.
        return mICallImpl;
    }
}
