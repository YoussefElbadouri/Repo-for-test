import java.io.*;

class Exploit implements Serializable {
    private static final long serialVersionUID = 1L;
    private String cmd;

    public Exploit(String cmd) {
        this.cmd = cmd;
    }

    private Object readResolve() {
        Runtime.getRuntime().exec(cmd); // ❌ Injection de commande possible !
        return this;
    }
}
