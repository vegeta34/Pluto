
#import cv2
#import sys
#sys.path.append("game/")
#import wrapped_flappy_bird as game
#from BrainDQN_Nature import BrainDQN
import numpy as np
import gym
import time
import cv2
#import drl
import os
import drl
from wetest import device
#from irl import wtirler
from collections import deque

render = False
GAMMA = 0.99
STATE_NUM = 4
MAX_STEPS = 32

# preprocess raw image to 80*80 gray image to 6400 1D vector
def preprocess(observation):
    observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
    #ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    #return np.reshape(observation,(80,80,1))
    return np.reshape(observation,(6400,1))

def prepro(I):
    """ prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector """
    I = I[35:195]
    I = I[::2,::2,0]
    I[I == 144] = 0
    I[I == 109] = 0
    I[I != 0] = 1
    return I.astype(np.float).ravel()
'''
def playGame():
    # Step 1: init BrainDQN
    #actions = 2
    actions = 3
    #brain = BrainDQN(actions)
    brain = WTDQN(actions)
    # Step 2: init Game
    env = gym.make("Pong-v0")
    observation = env.reset()
    #flappyBird = game.GameState()
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
    while 1!= 0:
        env.render()
        action = brain.getAction()
        #nextObservation,reward,terminal = flappyBird.frame_step(action)
        observation, reward, terminal, _ = env.step(action + 1)
        reward_sum += reward
        action_arr = np.zeros(actions)
        action_arr[action] = 1
        brain.setPerception(preprocess(observation),action_arr,reward,terminal)
        if reward != 0:
            print (('episode %d: game %d took %.5fs, reward: %f' %
                (episode_number, game_number,
                time.time()-start_time, reward)),
                ('' if reward == -1 else ' !!!!!!!!'))
            start_time = time.time()
            brain.onGameOver()
        if terminal == True:
            episode_number +=1
            game_number = 0
            running_reward = reward_sum if running_reward is None else running_reward * 0.99 + reward_sum * 0.01
            print('resetting env. episode reward total was %f. running mean: %f' % (reward_sum, running_reward))
            reward_sum = 0
            env.reset()
        #nextObservation = preprocess(nextObservation)
        #brain.setPerception(nextObservation,action,reward,terminal)
'''

def process_expert_data():
    miu = None
    first_miu = True
    miu_count = 0
    for i in range(1, 100):
        if os.path.exists('mldata/trajectory_%d' %(i)) == False:
            break
        miu_count += 1
        #currentState = np.stack((observation, observation, observation, observation), axis = 2)
        first_flag = True
        current_state = deque()
        count = 0
        for j in range(0, 300):
            imgpath = 'mldata/trajectory_%d/SM-N9200_0815f81337e81502/snapshot/l%d.jpg' %(i, j)
            if os.path.exists(imgpath) == False:
                continue
            img = cv2.imread(imgpath)
            img = preprocess(img)
            if first_flag == True:
                current_state.append(img)
                current_state.append(img)
                current_state.append(img)
                current_state.append(img)
                first_flag = False
            else:
                #current_state = np.append(current_state[:,:,1:],img,axis = 2)
                current_state.append(img)
                current_state.popleft()
            state = np.array([current_state[0], current_state[1], current_state[2], current_state[2]])
            state = np.reshape(state,(25600))
            if first_miu == True:
                miu = np.power(GAMMA, count) * state
                first_miu = False
            else:
                miu = miu + np.power(GAMMA, count) * state
            count += 1
    miu = miu / miu_count
    print miu.shape
    return miu

def randomplay():
    actions = 80 * 80
    mydevice = device.get_device()
    mydevice.launch_app()
    observation = mydevice.screenshot()
    for i in range(0, 8):
        for j in range(0, MAX_STEPS):
            action = random.randrange(actions)
            mydevice.takeaction(action)
            mydevice.screenshot()


#inverse reinforcement algorithm
def irl_process():
    miu_e = process_expert_data() #miu generated from human data
    #irl_processer = wtirler(miu_e)
    #miu = irl_processer.generate_miu(None)  #null means random play
    miu = randomplay()
    epsilon = 0.001
    t = 100
    tmiu = None
    while True:
        #w, t = irl_processer.process(miu)
        if tmiu == None:
            tmiu = miu
        else:
            tmiu = tmiu + ((miu - tmiu)*(miue - tmiu)/(miu - tmiu)*(miu - tmiu))*(miu - tmiu)
        w = miue - tmiu
        t = np.float_power(np.sum(np.square(w)))
        if t < epsilon:
            break
        brain = WTDQN(actions)
        drl.playGame(w, brain)  #using Reward function with parameter w
        miu_tmp = miu

        miu = drl.playGame(w, brain)


def main():
	irl_process()

if __name__ == '__main__':
	main()
