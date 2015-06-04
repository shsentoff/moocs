// IRequest.aidl
package us.sentoff.testserviceexec;

// Declare any non-default types here with import statements
import us.sentoff.testserviceexec.IReply;

/**
 * To make a request
 */
interface IRequest {
    /**
     * Make the request and pass an interface to use for replies.
     */
     oneway void getStuff(in int input, in IReply reply);
}
