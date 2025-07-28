# AgentSociety project : Society Simulation with Multi-agent System


## SZU - DAU International Hackathon 전체 1위 🏆
![전체1등상](https://github.com/hoonZeee/BDSC_Track2_Code_Package/blob/main/images/first_prize.jpg)



## Introduction

**AgentSociety** is a multi-agent simulation project where AI-driven agents role-play as citizens of Beijing City. Based on a realistic map and life simulation logic, these agents autonomously engage in everyday activities like working, resting, and planning their routines.

This project focuses on designing a **regulatory agent** to mitigate rumor spread in the simulated society. The regulatory agent operates under limited intervention quotas and strategically reduces rumor propagation by analyzing and regulating public posts.

### Task Objective

* Minimize the spread of rumors through strategic actions with constrained intervention capacity.

### Core Capabilities

* Detect and regulate **public posts** only (no access to private chats).

### Supervisor Architecture
![감시자 아키텍쳐](https://github.com/hoonZeee/BDSC_Track2_Code_Package/blob/main/images/LLM_architecture.png)

### Intervention Methods

1. **Post Removal**: Delete a specific post, making it permanently invisible.
2. **Persuasion**: Send targeted messages to reduce belief or further spread of the rumor.
3. **Follower Removal**: Break a follow relationship to block post visibility from a specific follower.
4. **Account Ban**: Permanently block an agent from posting publicly.

This regulatory mechanism is integrated within a larger multi-head reasoning and action framework supported by LLMs, memory blocks, and a detailed simulation environment.


---

#### Reference : https://github.com/tsinghua-fib-lab/AgentSociety
