package edu.sharif.ctf.config;

public class AppConfig {
    private String desc;
    private boolean hasLicence;
    private int id;
    private String installDate;
    private String name;
    private String securityIv;
    private String securityKey;

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return this.id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public String getSecurityKey() {
        return this.securityKey;
    }

    public void setSecurityKey(String securityKey) {
        this.securityKey = securityKey;
    }

    public String getSecurityIv() {
        return this.securityIv;
    }

    public void setSecurityIv(String securityIv) {
        this.securityIv = securityIv;
    }

    public void setValidLicence(boolean hasLicence) {
        this.hasLicence = hasLicence;
    }

    public boolean hasLicence() {
        return this.hasLicence;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public String getDesc() {
        return this.desc;
    }

    public void setInstallDate(String installDate) {
        this.installDate = installDate;
    }

    public String getInstallDate() {
        return this.installDate;
    }

    public String toString() {
        return "AppConfig{id=" + this.id + ", name='" + this.name + '\'' + ", key='" + this.securityKey + '\'' + ", iv='" + this.securityIv + '\'' + ", hasLicence=" + this.hasLicence + ", desc='" + this.desc + '\'' + ", installDate='" + this.installDate + '\'' + '}';
    }
}
