# -------------------------
# Project: Deep Q-Learning on Flappy Bird
# Author: Flood Sung
# Date: 2016.3.21
# -------------------------

#import cv2
#import sys
#sys.path.append("game/")
#import wrapped_flappy_bird as game
#from BrainDQN_Nature import BrainDQN
from wt_drl import WTDQN
import numpy as np
import gym
import time
import cv2

render = False

# preprocess raw image to 80*80 gray image
def preprocess(observation):
	observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
	return np.reshape(observation,(80,80,1))

def prepro(I):
    """ prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector """
    I = I[35:195]
    I = I[::2,::2,0]
    I[I == 144] = 0
    I[I == 109] = 0
    I[I != 0] = 1
    return I.astype(np.float).ravel()

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

def irl_process():
    miu_e = compute_miu(human_data) #miu generated from human data
    miu = generate_miu(Null)  #null means random play
    epsilon = 0.001
    t = 100
    for True:
       w, t = irl_linear(miu_e, miu) #linear method irl
       if t < epsilon:
           break
       pi = rl_process(w)  #using Reward function with parameter w
       miu_tmp = miu
       miu = generate_miu(pi)
       miu = miu_tmp + ((miu - miu_tmp)*(miu_e - miu_tmp)/(miu - miu_tmp)*(miu - miu_tmp))*(miu - miu_tmp))

def main():
	playGame()

if __name__ == '__main__':
	main()
