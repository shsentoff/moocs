package us.sentoff.testserviceexec;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MyService extends Service {
    private final static String TAG = "MyService";

    public MyService() {
    }

    // Create the stub for handling the request.
    // This is sent from onBind, so that the proxy can send us requests.
    private final IRequest.Stub mIRequestImpl = new IRequest.Stub() {
        @Override
        public void getStuff(final int input, final IReply iReply) throws RemoteException {
            Log.d(TAG, "started: " + Thread.currentThread());

            try {
                iReply.started(input);
            } catch (RemoteException e) {
                e.printStackTrace();
            }

            // Wait
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            Log.d(TAG, "finished: " + Thread.currentThread());

            // Pass back the answer.
            try {
                iReply.finished(input + 1000);
            } catch (RemoteException e) {
                e.printStackTrace();
            }

        }
    };

    @Override
    public IBinder onBind(Intent intent) {
        // Return the communication channel to the service.
        return mIRequestImpl;
    }
}
