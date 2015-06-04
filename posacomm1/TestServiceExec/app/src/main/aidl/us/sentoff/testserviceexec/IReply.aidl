// IReply.aidl
package us.sentoff.testserviceexec;

/**
 * For replying from the service.
 */
interface IReply {
    /*
     * Tell the client we started.
     */
    oneway void started(in int input);

    /**
     * Pass back the result to the client.
     */
    oneway void finished(in int output);
}
