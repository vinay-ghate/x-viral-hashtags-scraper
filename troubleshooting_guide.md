# Troubleshooting Cloud Deployment

If you are unable to access your FastAPI application running on a cloud server, follow these steps to identify and fix the issue.

## 1. Verify the Application is Running
First, ensure the application started successfully without errors.
- Check the terminal output where you ran the command. It should say something like:
  ```
  INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
  ```
- If it crashed, check the error message.

## 2. Test Locally on the Server
Try to access the application *from within the server* to confirm it's listening correctly.
Open a second terminal on the server and run:
```bash
curl http://localhost:8001/docs
```
- **If this works (returns HTML):** The app is running fine. The issue is with the network/firewall.
- **If this fails (Connection refused):** The app is not running or not listening on the expected port.

## 3. Check Firewall / Security Groups (Oracle Cloud Specifics)
Since you are using **Oracle Cloud**, there are **TWO** layers of firewalls you must configure. It is very common to fix one and forget the other.

### Layer 1: Oracle Cloud Console (VCN Security List)
1.  Log in to the Oracle Cloud Console.
2.  Go to **Networking** -> **Virtual Cloud Networks**.
3.  Click on your VCN, then click on **"Security Lists"** (usually "Default Security List").
4.  Click **"Add Ingress Rules"**.
5.  Add a rule with:
    *   **Source CIDR:** `0.0.0.0/0`
    *   **IP Protocol:** TCP
    *   **Destination Port Range:** `8001`
6.  Save the rule.

### Layer 2: Instance OS Firewall (The "Hidden" Blocker)
Oracle Cloud images (especially Ubuntu and Oracle Linux) come with strict `iptables` rules by default that block ports **even if the Security List allows them**.

**Run these commands on your server:**

**Option A: If using Ubuntu (UFW)**
```bash
sudo ufw allow 8001/tcp
sudo ufw reload
```

**Option B: If using Oracle Linux / CentOS / RHEL (Firewalld)**
```bash
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --reload
```

**Option C: If using raw iptables (Common on OCI)**
If the above don't work, you might need to edit iptables directly.
1.  Check current rules: `sudo iptables -L --line-numbers`
2.  Insert a rule to accept port 8001 (usually at the top or before the REJECT lines):
    ```bash
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8001 -j ACCEPT
    sudo netfilter-persistent save
    ```
    *(Note: The index `6` is an example; ensure you insert it before any "REJECT" or "DROP" rules).*

## 4. Verify Public IP
Ensure you are using the correct **Public IP** address of your server.
- Do not use the private IP (often starts with `10.x`, `172.x`, or `192.168.x`).
- Test in your browser: `http://<YOUR_PUBLIC_IP>:8001/docs`
- **Note:** Make sure to use `http://` and NOT `https://` (unless you set up SSL). Browsers sometimes default to HTTPS.

## 5. Check Process Binding
Verify the process is actually listening on `0.0.0.0` (all interfaces) and not just `127.0.0.1` (localhost).
Run:
```bash
sudo netstat -tulpn | grep 8001
```
You should see `0.0.0.0:8001`.

## Summary Checklist
- [ ] App is running (no crash logs).
- [ ] `curl localhost:8001` works on the server.
- [ ] Cloud Security Group allows Inbound TCP 8001.
- [ ] Server firewall (`ufw`) allows 8001.
- [ ] Using Public IP with `http://`.
