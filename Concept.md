

# Multibody dynamics equation

 The **multibody dynamics equation** describes how these muscle forces generate movement, consisting of joint angles ($q$), their derivatives, muscle-tendon forces, and the moment arm ($r$):$$M(q) \cdot \ddot{q} + C(q, \dot{q}) \cdot \dot{q} + G(q) = \tau $$

# Muscle-tendon force

The muscle-tendon unit force is calculated by multiplying the fiber force by the cosine of the pennation angle. This angle represents the geometric orientation of the muscle fibers relative to the tendon's line of action: $$ F_{m} = a \cdot f_{a}(l) \cdot f_v(\dot{l}) + f_{p}(l) $$

The muscle fiber force is defined as the sum of the active and passive muscle forces: $$ F_m = F_{active} + F_{passive} $$

Specifically, the active muscle force is defined as the product of the muscle activation, the force-length relationship, and the force-velocity relationship, scaled by the maximum isometric force $F_{max}$: $$F_{active} = F_{max}[ a \cdot f_{l}(l) \cdot f_{v}(\dot{l})] $$

The muscle activation ($a$) represents the physiological state of the muscle, which accounts for the neural control signal ($u$) and the time constants associated with activation and deactivation dynamics ($\tau(u, a)$): $$ \dot{a} = \frac{(u - a)}{\tau (u, a)}$$

The passive muscle force represents the internal elastic properties of the muscle and depends on the fiber length:$$F_{passive} = F_{max} [ f_{p}(l) ]$$

# Inverse dynamics

Inverse dynamics is a process for calculating moment to make next joint angle given previous joint angle.

With the **multi-body dynamics equation**, you don't need to solve differential equation. We can get the torque involving movement with joint angle and their derivatives and multi-body configuration.

# Muscle redundancy

The human body utilizes multiple muscles to actuate a single joint. For instance, elbow flexion involves the coordinated action of not only the biceps brachii but also the brachialis and brachioradialis. Consequently, the number of unknown variables (muscle forces) exceeds the number of available equations (joint torques), leading to an under-determined system. Mathematically, this implies that an infinite number of muscle activation combinations can produce a specific target torque, a challenge commonly referred to as the muscle redundancy problem.

**Static optimization**

To resolve the redundancy problem, optimization methods are employed based on the hypothesis that the central nervous system selects the most efficient activation pattern among infinite possible solutions. Specifically, Static Optimization seeks a combination of muscle activations that minimizes a specific cost function at each time step, such as the sum of squared activations:$$\min \sum a_i^2$$

While this method is computationally efficient and fast, it struggles to fully account for the time-dependent, intrinsic muscle dynamics (e.g., activation and contraction dynamics).

**Computed Muscle Control**

Computed Muscle Control is a more integrated approach. It first calculates the desired joint torques required to achieve a specific acceleration—often using PD control to track a reference trajectory—and then distributes these torques among individual muscles. This distribution process explicitly accounts for the non-linear force-length-velocity relationships of each muscle-tendon unit.

# PD Controller

A PD controller is a type of feedback control system that uses two control algorithms: proportional and derivative. 

The proportional component of the controller is based on the current error between the desired setpoint and the actual value of the system being controller. Its primary goal is to provide a rapid response to acheive the target. The control output is determined by the error between the desired and actual states, which is then amplified by a proportional factor $K_p$.

Derivative Component: While the proportional controller focuses on rapid transition, the derivative component is responsible for smooth and stable control. Specifically, this controller responds to the rate of change (derivative) of the error.

**Example - Refrigerator**

Let's see one example. We need to keep the temperature of the fridge at 60 degrees. And the ambient temperature is 70. We can describe how ambient temperature affects the fridge with the following Differential Equation.

$$ \dot{y} = -k(y - 70) $$

If we want to keep the temperature at 60, a control strategy would be to decrease temperature when it’s over 60 and increase temperature otherwise. Resulting in the following system where $K_p$ is the proportional coefficient to be tuned:

$$ \dot{y} = -k(y - 70) + K_p(60 - y) $$

However, the system’s equilibrium depends on the $K_p$ parameter and is in fact never at 60:

$$\begin{aligned}
\dot{y} = 0 & = -k(y - 70) + K_p(60 - y) \\
0 & = -y(k + K_p) + 70k + 60K_p \\
y & = \frac{70k + 60K_p}{k + K_p}
\end{aligned}$$

$k = 0$ or $K_p \rightarrow \inf$

To fix this, we could modify our target term:

$$ Target = \frac{60k + 60K_p - 70k}{K_p}$$
$$\begin{aligned}

\dot{y} = 0 & = -k(y - 70) + K_p(Target - y) \\
0 & = -k(y - 70) + K_p(\frac{60k + 60K_p - 70k}{K_p} - y)
y(k + K_p) & = 70k + 60k + 60K_p - 70k
y & = 60
\end{aligned}$$

Adding derivative controller: $$ \dot{y} = -k(y - 70) + K_p(60-y) + K_d(\frac{60 - y}{dt}) $$