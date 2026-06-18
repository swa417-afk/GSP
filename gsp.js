
import { Router } from "express";
import { authRequired } from "../middleware/auth.js";
import { createAttestation } from "../utils/gspAttestation.js";

const router = Router();

router.get("/status", authRequired, (req, res) => {
  const attestation = createAttestation(req.user.id, "STATUS_CHECK", {});

  res.json({
    gsp: "active",
    userId: req.user.id,
    attestation
  });
});

router.post("/actions/log", authRequired, (req, res) => {
  const { action, metadata } = req.body || {};
  const attestation = createAttestation(req.user.id, action || "CUSTOM", metadata || {});
  // In a full implementation this would be stored in an audit log table or external system.
  res.json({ ok: true, attestation });
});

export default router;
