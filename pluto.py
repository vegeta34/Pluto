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

    # Step 3.2: run the game
    while 1!= 0:
        env.render()
        action = brain.getAction()
        #nextObservation,reward,terminal = flappyBird.frame_step(action)
        observation, reward, terminal, _ = env.step(action)
        action_arr = np.zeros(actions)
        action_arr[action] = 1
        brain.setPerception(preprocess(observation),action_arr,reward,terminal)
        #nextObservation = preprocess(nextObservation)
        #brain.setPerception(nextObservation,action,reward,terminal)
    """
    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        #if resume:
        #    load_params = tl.files.load_npz(name=model_file_name+'.npz')
        #    tl.files.assign_params(sess, load_params, network)
        #network.print_params()
        #network.print_layers()

        start_time = time.time()
        game_number = 0
        while True:
            if render: env.render()

            cur_x = prepro(observation)

            x = cur_x - prev_x if prev_x is not None else np.zeros(D)
            x = x.reshape(1, D)
            prev_x = cur_x

            #prob = sess.run(
            #    sampling_prob,
            #    feed_dict={states_batch_pl: x}
            #)
            # action. 1: STOP  2: UP  3: DOWN
            #action = np.random.choice([1,2,3], p=prob.flatten())
            action = brain.getAction()

            observation, reward, done, _ = env.step(action)
            brain.setPerception(prepro(observation),action,reward,terminal)

            reward_sum += reward
            xs.append(x)            # all observations in a episode
            ys.append(action - 1)   # all fake labels in a episode (action begins from 1, so minus 1)
            rs.append(reward)       # all rewards in a episode
            if done:
                episode_number += 1
                game_number = 0

                if episode_number % batch_size == 0:
                    print('batch over...... updating parameters......')
                    epx = np.vstack(xs)
                    epy = np.asarray(ys)
                    epr = np.asarray(rs)
                    disR = tl.rein.discount_episode_rewards(epr, gamma)
                    disR -= np.mean(disR)
                    disR /= np.std(disR)

                    xs, ys, rs = [], [], []

                    sess.run(
                        train_op,
                        feed_dict={
                            states_batch_pl: epx,
                            actions_batch_pl: epy,
                            discount_rewards_batch_pl: disR
                        }
                    )


                if episode_number % (batch_size * 100) == 0:
                    tl.files.save_npz(network.all_params, name=model_file_name+'.npz')

                running_reward = reward_sum if running_reward is None else running_reward * 0.99 + reward_sum * 0.01
                print('resetting env. episode reward total was %f. running mean: %f' % (reward_sum, running_reward))
                reward_sum = 0
                observation = env.reset() # reset env
                prev_x = None

            if reward != 0:
                print(('episode %d: game %d took %.5fs, reward: %f' %
                            (episode_number, game_number,
                            time.time()-start_time, reward)),
                            ('' if reward == -1 else ' !!!!!!!!'))
                start_time = time.time()
                game_number += 1
    """

def main():
	playGame()

if __name__ == '__main__':
	main()
