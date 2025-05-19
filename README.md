This repo is working version of Dan Anderson's [sawtooth-simplewallet](https://github.com/danintel/sawtooth-simplewallet) in Sawtooth 1.2

### To Run System

1. **`docker-compose up `**
2. **`docker-compose run simplewallet-client bash`**: `simplewallet-client` 
3. **`docker-compose down`**

### Useful Sawtooth Commands

1. **`sawtooth keygen name`**
2. **`sawtooth state list --url=http://rest-api:8008`**
3. **`sawtooth block list --url=http://rest-api:8008`**

### Simplewallet Commands
Don't forget to create keys with **`sawtooth keygen`**
1. **`create-wallet name`**
2. **`balance name`**
3. **`deposit name value`**
4. **`withdraw name value`**
5. **`transfer name name1 value`**

If you are out of any linux distro use: **`python3 transfer.py name name1 value`**

## Usage Scenario

1. **Running Containers**: `docker-compose up`, you can check active containers with `docker ps -a`.

2. **Client App**: In a new terminal, run `docker-compose run simplewallet-client bash` to enter client bash.

3. **Keygen**: In client, run `sawtooth keygen name1` to generate key pairs. 

6. **Create Wallet**: In client, run `create-wallet name1` 

7. **Deposit**: In client, run `deposit jack amount` 

8. **Check Balance**: In client, run `balance name1` 

9. **Withdraw**: In client, run `withdraw jack amount` 

10. **Transfer**: In client, run `transfer name1 name2 amount` 

To exit from client bash use `exit`.