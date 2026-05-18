const commandInput = document.getElementById('command');
const runButton = document.getElementById('runButton');
const outputArea = document.getElementById('output');
const planArea = document.getElementById('plan');
const statusLabel = document.getElementById('status');

function setStatus(text, state = 'idle') {
  const statusText = statusLabel.querySelector('.status-text');
  const spinner = statusLabel.querySelector('.spinner');
  if (statusText) statusText.textContent = text;
  statusLabel.classList.remove('status--idle', 'status--success', 'status--error', 'status--running');
  statusLabel.classList.add(`status--${state}`);
  if (state === 'idle') {
    statusLabel.classList.add('status--running');
  } else {
    statusLabel.classList.remove('status--running');
  }
}

async function runCommand() {
  const command = commandInput.value.trim();
  if (!command) {
    setStatus('Enter a command first.', 'error');
    return;
  }

  // trigger agent visual animation
  const agentVisual = document.querySelector('.agent-visual');
  if (agentVisual) {
    agentVisual.classList.remove('animate');
    // force reflow then add
    void agentVisual.offsetWidth;
    agentVisual.classList.add('animate');
  }

  setStatus('Running...', 'idle');
  outputArea.textContent = '';
  planArea.textContent = '';

  // create a small burst to indicate start
  if (agentVisual) createBurst(agentVisual, {count: 6});

  const result = await window.api.runCommand(command);

  if (result.error) {
    setStatus('Error', 'error');
    outputArea.textContent = result.error + (result.raw ? `\nRaw: ${result.raw}` : '');
    return;
  }

  setStatus('Success', 'success');
  // brief success pulse
  if (agentVisual) {
    agentVisual.classList.add('success');
    setTimeout(() => agentVisual.classList.remove('success'), 700);
  }
  planArea.textContent = JSON.stringify(result.plan || [], null, 2);
  outputArea.textContent = (result.output || []).join('\n');

  // pulse panels to draw attention
  const panels = document.querySelectorAll('.panel');
  panels.forEach(p => {
    p.classList.remove('pulse');
    void p.offsetWidth;
    p.classList.add('pulse', 'enter');
    setTimeout(() => p.classList.remove('enter'), 700);
    setTimeout(() => p.classList.remove('pulse'), 900);
  });
}

runButton.addEventListener('click', runCommand);

commandInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    runCommand();
  }
});

// Copy buttons
const copyPlan = document.getElementById('copyPlan');
const copyOutput = document.getElementById('copyOutput');

function copyText(text) {
  return navigator.clipboard.writeText(text);
}

if (copyPlan) {
  copyPlan.addEventListener('click', async () => {
    await copyText(planArea.textContent || '');
    const prev = copyPlan.textContent;
    copyPlan.textContent = 'Copied';
    setTimeout(() => copyPlan.textContent = prev, 1400);
  });
}

if (copyOutput) {
  copyOutput.addEventListener('click', async () => {
    await copyText(outputArea.textContent || '');
    const prev = copyOutput.textContent;
    copyOutput.textContent = 'Copied';
    setTimeout(() => copyOutput.textContent = prev, 1400);
  });
}

// Remove animate class after animation completes to allow retrigger
const agentVisual = document.querySelector('.agent-visual');
if (agentVisual) {
  agentVisual.addEventListener('animationend', (e) => {
    if (e.animationName === 'orb-wobble' || e.animationName === 'ring-echo') {
      agentVisual.classList.remove('animate');
    }
  });
}

// create burst and particles inside agent visual
function createBurst(container, opts = {}) {
  const count = opts.count || 8;
  const fragments = [];
  // ring
  const ring = document.createElement('div');
  ring.className = 'burst-ring';
  container.appendChild(ring);
  fragments.push(ring);

  for (let i = 0; i < count; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    // random angle and distance
    const angle = Math.random() * Math.PI * 2;
    const r = 36 + Math.random() * 48;
    const x = 50 + Math.cos(angle) * r;
    const y = 50 + Math.sin(angle) * r;
    p.style.left = x + '%';
    p.style.top = y + '%';
    p.style.background = `radial-gradient(circle at 30% 30%, rgba(255,255,255,0.95), rgba(110,170,255,${0.6+Math.random()*0.25}))`;
    container.appendChild(p);
    fragments.push(p);
  }

  // cleanup after animation
  setTimeout(() => {
    fragments.forEach(el => el.remove());
  }, 900);
}
