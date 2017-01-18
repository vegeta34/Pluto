
from wt_drl import WTDQN
import numpy as np
from device.wetest import device
import image
from collections import deque

MAX_STEPS = 128
MAX_REWARD_MEMORY_SIZE = 4

#used to calculate reward
experience_queue = deque()

def getCurrentReward(reward_w):
    a = np.array(experience_queue[0], experience_queue[1], experience_queue[2], experience_queue[3])
    return np.dot(a.flatten(), reward_x)


#play game using DRL
def playGame(reward_w):
    # Step 1: init BrainDQN
    #actions = 2
    actions = 80 * 80
    #brain = BrainDQN(actions)
    brain = WTDQN(actions)
    # Step 2: init Game
    #env = gym.make("Pong-v0")
    #observation = env.reset()
    #flappyBird = game.GameState()
    mydevice = device.get_device()
    mydevice.launch_app()
    observation = mydevice.screenshot()
    # Step 3: play game
    # Step 3.1: obtain init state
    #action0 = np.array([1,0])  # do nothing
    #observation0, reward0, terminal = flappyBird.frame_step(action0)
    observation0 = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
    #brain.setInitState(observation0)
    brain.setInitState(observation0)
    game_number = 0
    episode_number = 0
    start_time = time.time()
    reward_sum = 0
    running_reward = None
    # Step 3.2: run the game
    #while 1!= 0:
    for:
        for i=0; i< MAX_STEPS; i++:
            env.render()
            action = brain.getAction()
            #nextObservation,reward,terminal = flappyBird.frame_step(action)
            #observation, reward, terminal, _ = env.step(action + 1)
            mydevice.action(action)
            observation = mydevice.snapshot()
            if experience_queue.count >= MAX_REWARD_MEMORY_SIZE:
                experience_queue.popleft()
            experience_queue.append(image.preprocess(observation))
            reward = getCurrentReward()
            reward_sum += reward
            action_arr = np.zeros(actions)
            action_arr[action] = 1
            brain.setPerception(image.preprocess(observation),action_arr,reward,terminal)
            if reward != 0:
                print (('episode %d: took %.5fs, reward: %f' %
                    (episode_number, time.time()-start_time, reward)),
                    ('' if reward == -1 else ' !!!!!!!!'))
                start_time = time.time()
                brain.onGameOver()
        experience_queue.clear()
        episode_number +=1
        #game_number = 0
        running_reward = reward_sum if running_reward is None else running_reward * 0.99 + reward_sum * 0.01
        print('resetting env. episode reward total was %f. running mean: %f' % (reward_sum, running_reward))
        reward_sum = 0
        #env.reset()
        #nextObservation = preprocess(nextObservation)
        #brain.setPerception(nextObservation,action,reward,terminal)

