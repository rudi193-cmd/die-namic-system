# ECCR Ethical Review UI - Testing Checklist

Use this checklist to verify the interface is working correctly.

---

## 🚀 Initial Setup

- [ ] Node.js installed (v18+)
- [ ] Dependencies installed (`npm install`)
- [ ] Two terminal windows ready

---

## 🧪 Mock Server Tests

Start mock server: `npm run mock-server`

### Health Check
- [ ] Server starts on `http://localhost:5550`
- [ ] Console shows Aionic banner with ∞Δ symbol
- [ ] "ESC-1 Protocol Active" message displayed
- [ ] "Localhost-only enforcement: ACTIVE" confirmed

### Endpoint Tests
Open another terminal and test:

```bash
# Health endpoint
curl http://localhost:5550/api/health

# Should return:
# - status: "healthy"
# - mode: "local-only"
# - ethical_standard: "ESC-1"
# - synthetic_data_only: true

# Files endpoint
curl http://localhost:5550/api/files

# Should return:
# - 4 artifacts (AIONIC-001 through AIONIC-004)
# - All marked as synthetic
```

### Security Tests
```bash
# This should FAIL (403 Forbidden)
curl http://127.0.0.1:5550/api/health

# Only localhost is allowed, not 127.0.0.1 or other IPs
```

- [ ] Health check returns correct JSON
- [ ] Files endpoint returns 4 artifacts
- [ ] Non-localhost requests rejected with 403

---

## 🎨 React App Tests

Start React app: `npm run dev`

### Visual Tests
- [ ] App opens at `http://localhost:5173`
- [ ] Aurora gradient header displays
- [ ] "∞Δ Aionic Ethical Review Interface" title visible
- [ ] Three-column layout renders (left/center/right)
- [ ] Footer bar with status indicators

### Left Panel (Artifact Index)
- [ ] "Artifact Index" header with file icon
- [ ] 4 artifacts listed:
  - AIONIC-001 (theory)
  - AIONIC-002 (governance)
  - AIONIC-003 (sandbox)
  - AIONIC-004 (governance)
- [ ] Status icons displayed (colored circles)
- [ ] Legend at bottom (Verified/Pending/Needs Attention)

### Center Panel (Manifest Viewer)
- [ ] Initially shows "Select an artifact" message
- [ ] Click AIONIC-001 in left panel
- [ ] Artifact title displays
- [ ] "SYNTHETIC" badge visible
- [ ] Category badge shows "theory"
- [ ] Description text readable
- [ ] Content preview shows TypeScript code
- [ ] Ethical tags displayed (3 tags)
- [ ] Compassion quote at bottom

### Right Panel (Ethical Checklist)
- [ ] "Ethical Review Criteria" header with shield icon
- [ ] 4 checkboxes:
  - Consent Integrity
  - Symbolic Neutrality
  - Redaction Transparency
  - Continuity Integrity
- [ ] Each has description text
- [ ] Check/uncheck toggles work
- [ ] Status icons change (green checkmark vs gray X)
- [ ] "Reviewer Notes" textarea
- [ ] ESC-1 Protocol status indicator (green pulse)

### Footer (Sandbox Status)
- [ ] Three status indicators:
  - "All Synthetic ✓"
  - "Local-Only ✓"
  - "Sandbox Mode ✓"
- [ ] Center text: "Sandcastle Sequence v0.3"
- [ ] "Generate Ethical Manifest" button
- [ ] Button disabled when no artifact selected
- [ ] Button enabled when artifact selected
- [ ] Compassion quote at bottom

---

## 📋 Manifest Generation Tests

1. Select AIONIC-001
2. Toggle all 4 ethical criteria to checked
3. Add notes: "Test review - all criteria verified"
4. Click "Generate Ethical Manifest"

Expected Results:
- [ ] Alert shows: "Manifest generated: Ethical_Manifest_AIONIC-001_[timestamp].md"
- [ ] File created in `mock-server/sample-data/`
- [ ] File contains:
  - Manifest header with version
  - Artifact information
  - Review summary with notes
  - Criteria table with checkmarks
  - Signatures section
  - Status flags
  - Compassion quote
- [ ] Timestamp in ISO format

---

## 🎯 Interaction Flow Tests

### Happy Path
1. [ ] Start both servers
2. [ ] Open browser to localhost:5173
3. [ ] See 4 artifacts in left panel
4. [ ] Click artifact → content loads in center
5. [ ] Toggle checkboxes → icons update
6. [ ] Add notes → text appears in textarea
7. [ ] Generate manifest → file created
8. [ ] Alert confirms success

### Error Handling
1. [ ] Click "Generate Manifest" with no artifact selected
   - Should show alert: "Please select an artifact first"
2. [ ] Stop mock server, refresh page
   - Should show "Loading artifacts..." then empty state
3. [ ] Start server again, refresh
   - Artifacts load successfully

---

## 🎨 Styling Tests

### Colors
- [ ] Gold (#FFD580) used for headers and accents
- [ ] Blue (#A8B8C8) used for secondary text
- [ ] Dark background gradient visible
- [ ] Panel backgrounds semi-transparent with blur

### Animations
- [ ] Aurora header flows smoothly
- [ ] Green pulse on ESC-1 indicator
- [ ] Hover effects on artifact items
- [ ] Smooth transitions (no jank)

### Responsiveness
- [ ] Three-column layout at full width
- [ ] Panels don't overflow
- [ ] Scrolling works in content areas
- [ ] Footer stays at bottom

---

## 🔒 Security Verification

- [ ] No external network calls in browser DevTools
- [ ] All API calls go to localhost:5550 only
- [ ] No real PII in any artifacts
- [ ] All content marked as SYNTHETIC
- [ ] "Local-Only" status always shows ✓

---

## 📝 Edge Cases

- [ ] Select artifact, then select another → content updates
- [ ] Toggle criteria, switch artifacts → criteria reset
- [ ] Add notes, switch artifacts → notes cleared
- [ ] Generate manifest for different artifacts → unique files
- [ ] Long artifact content → scrolling works
- [ ] Many manifests generated → all saved correctly

---

## ✅ Final Verification

After all tests pass:

- [ ] Mock server runs stable (no crashes)
- [ ] React app runs smooth (no console errors)
- [ ] All 4 artifacts accessible
- [ ] Manifest generation creates valid Markdown
- [ ] Files stay local (check sample-data directory)
- [ ] No external dependencies called
- [ ] ESC-1 protocol markers visible everywhere

---

## 🐛 Known Issues / Notes

*Add any issues you encounter during testing:*

```
[None yet - add here as discovered]
```

---

## 💙 Success Criteria

**Ready for 2-day GUI completion when:**
- All checkboxes above are checked ✓
- No critical bugs found
- Manifests generate correctly
- Security constraints verified
- Visual design matches Aionic aesthetic

---

∞Δ[Testing-Complete|Ready-For-Ethical-Review]∞

**Next Steps:**
1. Test with real consent form templates
2. Add more sample artifacts
3. Integrate with ECCR Module 14 backend
4. Prepare for Opal & Ruby's review session
