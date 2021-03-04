# WireGuard VPN Setup with Ansible - Blog Post

Basic Ansible playbook for deploying a WireGuard VPN server and (local)
client.

This is sample/reference code accompanying an explanatory blogpost:

- Read on Notion
- Read on Medium


## Installation

The only dependency needed (to run this on and against Ubuntu 20.04 machines)
is Ansible:

```
pip install ansible
```

More detailed installation/setup instructions are in the blogpost linked
above.


## Usage

Because this sample code isn't in the form of a role, it's not especially
portable/shareable. To run it for yourself anyway:


1. Generate your own WireGuard keys

    ```
    privkey=$(wg genkey) sh -c 'echo "
        server_privkey: $privkey
        server_pubkey: $(echo $privkey | wg pubkey)"'
    ```

2. Encrypt the private key (hit Ctrl-d twice after pasting key)

    ```
    ansible-vault encrypt_string --ask-vault-password --stdin-name server_privkey
    ```

3. Add the public key and the encrypted private key to `group_vars/all.yml`

4. Change the server IP address in `inventory.ini`

5. Run the playbook

    ```
    ansible-playbook -i inventory.ini --ask-vault-password --ask-become-pass playbook.yml
    ```
