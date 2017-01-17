
#import cv2
#import sys
#sys.path.append("game/")
#import wrapped_flappy_bird as game
#from BrainDQN_Nature import BrainDQN
import numpy as np
import gym
import time
import cv2
import drl

render = False
GAMMA = 0.99
STATE_NUM = 4

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

def process_expert_data(trajectories):
    print len(trajectories)
    m = len(trajectories)  #number of trajectories
    miu = 0
    for i = 0; i < len(trajectories); i++:
        currentState = np.stack((observation, observation, observation, observation), axis = 2)
        for j = 0; j < len(trajectories[i]); j++:
            currentState = np.append(currentState[:,:,1:],trajectories[i][j],axis = 2)
            state = np.reshape(currentState,(25600))
            miu += np.power(GAMMA, j) * state
    miu = miu / m
    return miu
    
#inverse reinforcement algorithm
def irl_process():
    human_data = read_data_from_file()
    miu_e = process_expert_data(human_data) #miu generated from human data
    irl_processer = WTIRL(miu_e)
    miu = irl_processer.generate_miu(None)  #null means random play
    epsilon = 0.001
    t = 100
    for True:
        w, t = irl_processer.process(miu)
        if t < epsilon:
            break
        pi = drl.playGame(w)  #using Reward function with parameter w
        miu_tmp = miu
        miu = irl_processer.generate_miu(pi)

def main():
	irl_process()

if __name__ == '__main__':
	main()
