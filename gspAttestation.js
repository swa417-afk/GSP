
import crypto from "crypto";
import dotenv from "dotenv";

dotenv.config();

export function createAttestation(userId, action, metadata = {}) {
  const issuer = process.env.GSP_ATTESTATION_ISSUER || "GSP";
  const timestamp = new Date().toISOString();

  const payload = {
    issuer,
    userId,
    action,
    metadata,
    timestamp
  };

  const hash = crypto
    .createHash("sha256")
    .update(JSON.stringify(payload))
    .digest("hex");

  return {
    ...payload,
    hash
  };
}
