import crypto from 'crypto';

class DataProtection {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32; // for 256-bit key
    this.ivLength = 16; // for AES
    this.saltLength = 64;
    this.tagLength = 16;
  }

  async hashPassword(password) {
    const salt = crypto.randomBytes(this.saltLength);
    return new Promise((resolve, reject) => {
      crypto.scrypt(password, salt, this.keyLength, (err, derivedKey) => {
        if (err) reject(err);
        resolve(salt.toString('hex') + ':' + derivedKey.toString('hex'));
      });
    });
  }

  async verifyPassword(storedPassword, suppliedPassword) {
    const [salt, key] = storedPassword.split(':');
    return new Promise((resolve, reject) => {
      const keyBuffer = Buffer.from(key, 'hex');
      crypto.scrypt(suppliedPassword, Buffer.from(salt, 'hex'), this.keyLength, (err, derivedKey) => {
        if (err) reject(err);
        resolve(crypto.timingSafeEqual(keyBuffer, derivedKey));
      });
    });
  }

  encrypt(text, masterKey) {
    const iv = crypto.randomBytes(this.ivLength);
    const salt = crypto.randomBytes(this.saltLength);
    const key = crypto.scryptSync(masterKey, salt, this.keyLength);
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);
    const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
    const tag = cipher.getAuthTag();
    return salt.toString('hex') + ':' + iv.toString('hex') + ':' + encrypted.toString('hex') + ':' + tag.toString('hex');
  }

  decrypt(encryptedText, masterKey) {
    const [salt, iv, encrypted, tag] = encryptedText.split(':').map(part => Buffer.from(part, 'hex'));
    const key = crypto.scryptSync(masterKey, salt, this.keyLength);
    const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
    decipher.setAuthTag(tag);
    return decipher.update(encrypted) + decipher.final('utf8');
  }

  generateMasterKey() {
    return crypto.randomBytes(this.keyLength).toString('hex');
  }
}

export default DataProtection;
