// ICall.aidl
package us.sentoff.testserviceexec;

interface ICall {
    /**
     * Gets stuff using the synchronous interface.
     */
    int getStuff(in int input);
}
