import crypto from 'crypto';

if (!crypto.hash) {
  crypto.hash = function(algorithm, data, outputEncoding) {
    const hash = crypto.createHash(algorithm);
    hash.update(data);
    return hash.digest(outputEncoding || 'hex');
  };
}

export default crypto;