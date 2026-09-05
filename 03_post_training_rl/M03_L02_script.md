# Episode M03_L02: The Death of the Critic: How DeepSeek-R1 Trained with GRPO

**Series:** LLMOps & Agentic Engineering: From Foundation to Production-Scale Systems  
**Module:** 03 — Post-Training & Reinforcement Learning  
**Target Duration:** 16:30  
**Format:** YouTube Masterclass Deep-Dive (Mathematical Whiteboard, Memory Physics, PyTorch Implementation)  
**Tone:** High-energy, authoritative, mathematically rigorous. Deconstructing the architecture that changed post-training economics.

---

## Technical Overview & Pedagogical Objectives
- **The Core Problem:** Proximal Policy Optimization (PPO)—the standard RL algorithm behind InstructGPT and Claude—requires loading 4 separate neural networks into GPU cluster VRAM: the Actor, the Critic (Value network), the Reference Model, and the Reward Model. The Critic network, tasked with predicting token-level scalar expected returns $V(s_t)$, typically needs to be the exact same parameter size as the Actor, consuming half of the available cluster memory and doubling inter-node gradient communication.
- **The Algorithmic Breakthrough:** Group Relative Policy Optimization (GRPO), introduced by DeepSeek in the DeepSeekMath and DeepSeek-R1 architectures. GRPO completely eliminates the Critic model. For each query $q$, the Actor samples a group of $G$ outputs $\{o_1, \dots, o_G\}$. The Advantage of output $i$ is calculated by normalizing its reward against the group's empirical distribution:
  $$A_i = \frac{r_i - \mu_{\{r_1 \dots r_G\}}}{\sigma_{\{r_1 \dots r_G\}} + \epsilon}$$
- **The Working Demonstration:** A pure PyTorch implementation of the GRPO objective function, demonstrating group reward normalization, token-level probability ratio clipping, and direct KL divergence penalty computation without a Critic.

---

## Script & Production Timeline

### 00:00 - 00:50 | ACT I: The Memory Wall of PPO (The Hook)
**[VISUAL]** High-contrast 3D server rack animation.
- A cluster of 8x NVIDIA H100 80GB GPUs.
- Four large model blocks are loaded into memory:
  1. `Actor (70B BF16)`: 140 GB
  2. `Critic (70B BF16)`: 140 GB
  3. `Reference Model (70B BF16)`: 140 GB
  4. `Reward Model (70B BF16)`: 140 GB
  - Total VRAM required for weights alone: 560 GB!
  - Add optimizer states (AdamW: 8-16 bytes/param) and activation memory: **OUT OF MEMORY (OOM)** error flashes in red.
- A laser blade slices through the Critic and Reward models, dissolving them. Text appears: **"VRAM CUT BY 65% — INTRODUCING GRPO."**

**[AUDIO]** Pulsing cybernetic synth, building in intensity. Voice enters crisp, authoritative.

**[NARRATOR (VO)]**
> "When OpenAI released ChatGPT, the foundation of their alignment stack was an algorithm created in 2017 called PPO—Proximal Policy Optimization.
> 
> But for seven years, enterprise engineering teams trying to run PPO on their own infrastructure ran into a brutal physical wall: **The Four-Model Memory Wall**.
> 
> To train a single 70-billion-parameter LLM using PPO, you don't just load one 70B model into your cluster. You have to load four: the Actor, the Critic, the Reference model, and the Reward model.
> 
> The Critic model alone, which estimates the future value of every intermediate token, must be roughly as large as the Actor to be accurate. That single component doubles your GPU compute bill and requires dozens of extra H100s just to store weights and optimizer states.
> 
> In January 2025, DeepSeek published DeepSeek-R1 and shocked the AI world by matching closed-source frontier reasoning models.
> 
> How did they afford the reinforcement learning compute?
> 
> They didn't optimize the Critic. **They murdered the Critic.**
> 
> In this video, we derive the exact mathematics of Group Relative Policy Optimization (GRPO), explain how sampling candidate groups eliminates the Value network entirely, and code the full PyTorch loss function from scratch."

---

### 00:50 - 04:30 | ACT II: PPO vs. GRPO: The Architectural Anatomy
**[VISUAL]** Side-by-side architectural flow diagram:
- **Left: Standard PPO**
  - Prompt $q \to$ Actor generates single completion $o$.
  - Critic network $V_\phi(s_t)$ evaluates state value at every token step $t$.
  - Generalized Advantage Estimation (GAE): $\hat{A}_t = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}^V$.
  - Critic update requires its own mean-squared-error loss backprop.
- **Right: DeepSeek GRPO**
  - Prompt $q \to$ Actor generates $G$ parallel completions $\{o_1, o_2, \dots, o_G\}$ (typically $G=8$ or $16$).
  - Reward function evaluates each completion: $\{r_1, r_2, \dots, r_G\}$.
  - Advantage $A_i$ computed via scalar group normalization: $(r_i - \mu) / \sigma$.
  - Critic network: **DOES NOT EXIST.**

**[SCREEN TEXT]**
```text
PPO Memory Footprint:  Actor (Train) + Critic (Train) + Reference (Frozen) + Reward (Frozen) = 4 Models
GRPO Memory Footprint: Actor (Train) + Reference (Frozen) = 2 Models (50-65% VRAM Reduction)
```

**[NARRATOR (VO)]**
> "Let's look at why PPO needed a Critic in the first place.
> 
> In reinforcement learning, the Actor generates an action, and we want to update its weights so that actions leading to high rewards become more probable.
> 
> But reward signals are inherently noisy. If a student guesses the right answer on a multiple-choice math test by pure luck, you don't want to reinforce every random thought they had along the way.
> 
> That’s why RL uses **Advantage** instead of raw reward:
> 
> $$A(s, a) = Q(s, a) - V(s)$$
> 
> The Advantage tells us: how much better was this specific action compared to what we expected on average in this state?
> 
> In PPO, estimating that baseline expectation $V(s)$ requires training a massive Critic neural network. That Critic outputs a scalar prediction at every single token.
> 
> Think about the engineering nightmare of this: you are training two coupled 70-billion-parameter models simultaneously. If the Critic learns too slowly, its baseline estimates are garbage, causing the Actor's policy to destabilize. If the Critic overfits, the policy collapses.
> 
> DeepSeek looked at this and asked an audacious question:
> 
> *Why train a 70-billion-parameter neural network just to predict the average score of a prompt, when we can simply sample 8 completions from the model itself and calculate the literal empirical average in two lines of Python?*
> 
> That is the core insight of GRPO."

---

### 04:30 - 08:45 | ACT III: The Mathematical Derivation of GRPO
**[VISUAL]** Mathematical whiteboard. Formulas written cleanly with animated color callouts:
1. **Group Advantage Formula:**
   $$\mu = \frac{1}{G} \sum_{i=1}^G r_i, \quad \sigma = \sqrt{\frac{1}{G} \sum_{i=1}^G (r_i - \mu)^2}$$
   $$A_i = \frac{r_i - \mu}{\sigma + \epsilon}$$
2. **The GRPO Objective Function:**
   $$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{\substack{q \sim P(Q) \\ \{o_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(O \mid q)}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \left\{ \min\left( \frac{\pi_\theta(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid q, o_{i,<t})} A_i, \; \text{clip}\left(\frac{\pi_\theta}{\pi_{\theta_{\text{old}}}}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta D_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}}) \right\} \right]$$

**[NARRATOR (VO)]**
> "Let's examine the mathematical beauty of this equation.
> 
> Step one: For a given prompt $q$, we sample a group of $G$ outputs from our current policy $\pi_{\theta_{\text{old}}}$. In practice, $G$ is typically between 8 and 64.
> 
> Step two: We evaluate each output with our reward function to get scalar scores $r_1$ through $r_G$.
> 
> Step three: We calculate the mean $\mu$ and standard deviation $\sigma$ of those scores across the group.
> 
> The Advantage $A_i$ for candidate $i$ is simply:
> 
> $$A_i = \frac{r_i - \mu}{\sigma + \epsilon}$$
> 
> Notice what happens here:
> If output 1 scored a 1.0 (it passed all unit tests), and the other 7 outputs scored 0.0 (they failed), the mean is 0.125.
> Output 1 gets a large positive Advantage. The failed outputs get a negative Advantage.
> 
> We don't need a Critic network to tell us that output 1 was above average—the empirical group distribution already proved it!
> 
> Now, look at the outer objective function. Notice the probability ratio:
> 
> $$\frac{\pi_\theta(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid q, o_{i,<t})}$$
> 
> This is the exact same clipped surrogate objective from PPO that prevents the policy from updating too drastically in a single step.
> 
> And look at the final term: $-\beta D_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}})$.
> In standard PPO, the KL divergence penalty is added directly to the per-step reward, which the Critic must learn to predict.
> In GRPO, the KL divergence is calculated directly inside the loss function, comparing the token probabilities of the active Actor with the frozen Reference model.
> 
> The Critic is completely dead. No value network weights. No value network optimizer states. No value loss backpropagation."

---

### 08:45 - 13:30 | ACT IV: PyTorch Implementation & Tensor Inspection
**[VISUAL]** Visual Studio Code screen capture (`08_VIDEO_PROJECTS/grpo_loss_engine.py`).
Dark mode theme, JetBrains Mono font. Terminal on bottom showing output shapes and verified loss.

**[SCREEN CODE]**:
```python
import torch
import torch.nn.functional as F

def compute_grpo_loss(
    log_probs_active: torch.Tensor,      # [G, T] - Policy being updated
    log_probs_old: torch.Tensor,         # [G, T] - Rollout policy
    log_probs_ref: torch.Tensor,         # [G, T] - Frozen reference model
    rewards: torch.Tensor,               # [G]    - Scalar reward per sample
    mask: torch.Tensor,                  # [G, T] - Attention padding mask
    clip_eps: float = 0.2,
    beta_kl: float = 0.04
) -> tuple[torch.Tensor, dict]:
    G, T = log_probs_active.shape
    
    # 1. Compute Group Normalized Advantage: A_i = (r_i - mu) / (sigma + eps)
    mean_r = rewards.mean()
    std_r = rewards.std() + 1e-8
    advantages = (rewards - mean_r) / std_r  # Shape: [G]
    advantages = advantages.unsqueeze(-1)    # Shape: [G, 1]
    
    # 2. Probability Ratio: pi_theta / pi_old
    ratio = torch.exp(log_probs_active - log_probs_old)  # Shape: [G, T]
    
    # 3. Clipped Surrogate Objective
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * advantages
    policy_loss = -torch.min(surr1, surr2)  # Maximize objective -> Minimize negative
    
    # 4. Direct KL Divergence Penalty (Schulman approximation)
    # D_KL = exp(log_ref - log_act) - (log_ref - log_act) - 1
    log_ratio_kl = log_probs_ref - log_probs_active
    kl_div = torch.exp(log_ratio_kl) - log_ratio_kl - 1.0
    
    # 5. Total Masked Token Loss
    total_loss = policy_loss + beta_kl * kl_div
    masked_loss = (total_loss * mask).sum() / mask.sum()
    
    metrics = {
        "mean_reward": mean_r.item(),
        "advantage_std": std_r.item(),
        "mean_kl": (kl_div * mask).sum().item() / mask.sum().item()
    }
    return masked_loss, metrics
```

**[NARRATOR (VO)]**
> "Let's walk through the exact PyTorch implementation on screen.
> 
> Look at lines 15 through 18:
> We take our scalar tensor of rewards across the group of $G$ samples.
> We calculate `mean()` and `std()`, and normalize. That gives us our `advantages` tensor of shape `[G, 1]`. That advantage broadcasts across every token in that sample's sequence.
> 
> Next, line 21:
> We calculate the importance sampling ratio using log probabilities: `torch.exp(log_probs_active - log_probs_old)`.
> 
> Lines 24 through 26:
> We compute the classic PPO clipped surrogate objective: `torch.min(surr1, surr2)`. If the active policy attempts to make a token 500% more probable than it was during rollout, the clamp cuts it off at $1 + \epsilon$.
> 
> Now, look at line 30:
> Instead of training a Critic to predict token-level discounted rewards including KL penalties, we calculate the KL divergence directly between the Reference model and the Actor using John Schulman's unbiased estimator:
> `torch.exp(log_ratio_kl) - log_ratio_kl - 1.0`.
> 
> Finally, we apply our padding mask and sum.
> 
> Notice what is absent from this script:
> There is no Critic model forward pass.
> There is no Generalized Advantage Estimation (GAE) backward loop through time.
> There is no value function loss.
> 
> The entire training step runs in a fraction of the VRAM, allowing you to train reasoning models on a single 8x H100 node that previously required 32 GPUs."

---

### 13:30 - 16:30 | ACT V: The Unsloth Ecosystem & Next Steps
**[VISUAL]** Terminal displaying live training run using Unsloth AI's GRPO trainer on a GSM8K math dataset:
```bash
python -m unsloth.grpo \
    --model_name "Qwen/Qwen2.5-7B-Instruct" \
    --dataset "openai/gsm8k" \
    --num_generations 8 \
    --max_seq_length 2048 \
    --learning_rate 5e-6
```
Training progress shows GPU VRAM sitting comfortably at 28 GB out of 80 GB on an H100, generating 8 reasoning trajectories in parallel.

**[NARRATOR (VO)]**
> "With GRPO, the infrastructure barrier to training reasoning models has collapsed. Tools like Unsloth and Hugging Face TRL have packaged GRPO into single-line Python configurations.
> 
> You can now fine-tune a 7-billion or 14-billion parameter model with reinforcement learning on a single consumer GPU or a single cloud instance.
> 
> But eliminating the Critic network reveals an even more fundamental challenge in Reinforcement Learning:
> 
> **Where does the Reward signal come from?**
> 
> If you use a learned Reward Model—another neural network trained on human thumbs-up/thumbs-down preferences—you encounter 'Reward Hacking'. The LLM quickly discovers that using sycophantic, flowery language or generating 2,000 words of fake formatting tricks the reward model into giving it a perfect score.
> 
> To train true reasoning models, you must replace human preference models with **Deterministic Verifiable Rewards**.
> 
> Because you cannot smooth talk a compiler. You cannot flatter a Python interpreter. A unit test either passes or it fails.
> 
> In Episode 3, we dive into the science of Verifiable Rewards: how compilers, symbolic math engines, and AST parsers trigger the autonomous emergence of Chain-of-Thought reasoning.
> 
> Check out the GitHub repository in the description to run our `grpo_loss_engine.py` script locally.
> 
> Hit subscribe, and let's go build verifiable systems."
