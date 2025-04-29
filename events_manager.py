# %%
import numpy as np
import cv2


"""
Boxing:
- track when difference between player score and enemy score is +- 8 (10s before and 5s after)
- record when player and enemy score stagnates for at least 10s
- track when player hits enemy correctly for the first time (5s before and 10s after)

Turmoil:
- track when player score stagnates for at least 5s
- track 5s before and 5s after player dies
- track 5s before and after PRIZE acquisition
- track first time TANK enemy is killed (the one that can be killed from behind only)

Word Zapper:
- track when word completion stagnates for at least 7s
- 5s before and 10 after completion symbols are hit
- 5s before and after player is hit by asteroid for the first time (not implemented)
- 5s before and 7 after player is hit by deadly asteroid or shuffling asteroid (not implemented)

In general:
- first 30s of tutorial for each game

"""


# %%
def create_video(frames, filename, fps=30):
    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(
        filename,
        fourcc,
        fps,
        (width, height),
    )

    for j in frames:
        video.write(j)

    cv2.destroyAllWindows()
    video.release()


def remove_overlaps(segments):
    if not segments:
        return segments
    segments.sort(key=lambda x: x[0])
    result = [segments[0]]
    prev_start, prev_end = segments[0]
    for cur_start, cur_end in segments[1:]:
        # If current segment starts before or at the end of the previous segment,
        # adjust its start to prevent overlap.
        if cur_start <= prev_end:
            continue
            # cur_start = prev_end + 1
            # # Skip segment if it becomes too short or invalid.
            # if cur_start >= cur_end:
            #     continue
        result.append((cur_start, cur_end))
        prev_end = cur_end
    return result

####### General functions
# %%

def get_timeframe(data, start, end, fps=30):
    if len(data) < end:
        end = len(data)
    return [(start * fps, end * fps)]


####### boxing functions
# %%
def detect_box_score_difference(box_data, threshold=8, pre=10, post=5, fps=30):
    """Detect when the score difference reaches the threshold."""
    events = []
    for i in range(len(box_data)):
        player_score, enemy_score = box_data[i, 18], box_data[i, 19]
        if abs(player_score - enemy_score) >= threshold:
            start = max(0, i - (pre * fps))
        if abs (box_data[i-1, 18] - box_data[i-1, 19]) >= threshold and abs(player_score - enemy_score) < threshold:
            end = min(len(box_data), i + (post * fps))
            events.append((start, end))
    return remove_overlaps(events)
    # return events


# %%
def detect_box_score_stagnation(box_data, stagnation=10, fps=30):
    events = []
    start_idx = 0
    while start_idx < len(box_data):
        current_player = box_data[start_idx, 18]
        current_enemy = box_data[start_idx, 19]
        end_idx = start_idx
        # Extend while scores do not change
        while (
            end_idx < len(box_data)
            and box_data[end_idx, 18] == current_player
            and box_data[end_idx, 19] == current_enemy
        ):
            end_idx += 1
        if (end_idx - start_idx) >= stagnation * fps:
            events.append((start_idx, end_idx - 1))
        start_idx = end_idx
    return remove_overlaps(events)


def detect_box_first_hit(box_data, pre=5, post=10, fps=30):
    events = []
    for i in range(1, len(box_data)):
        if box_data[i - 1, 18] == 0 and box_data[i, 18] >= 1:
            start_frame = i - int(pre * fps)
            end_frame = min(
                i + int(post * fps), len(box_data) - 1
            )
            events.append((start_frame, end_frame))
            break  # Only record the first hit
    return events


############ turmoil functions


def detect_turmoil_score_stagnation(turm_data, stagnation=10, fps=30):
    events = []
    start_idx = 250
    while start_idx < len(turm_data):
        player_score = turm_data[start_idx, 9]
        end_idx = start_idx
        # Extend while scores do not change
        while end_idx < len(turm_data) and turm_data[end_idx, 9] == player_score:
            end_idx += 1
        if (end_idx - start_idx) >= stagnation * fps:
            events.append((start_idx, end_idx - 1))
        start_idx = end_idx
    return remove_overlaps(events)


def detect_turmoil_tank_destruction(turm_data, pre=10, post=5, fps=30):
    events = []
    appear = None
    destroyed = None
    for i in range(250, len(turm_data)):
        obstacles = turm_data[i, 62:69]

        if 10 in obstacles:
            if appear is None:
                appear = i
        else:
            if appear is not None:
                destroyed = i
                start_frame = appear - int(pre * fps)
                end_frame = min(
                    destroyed + int(post * fps), len(turm_data) - 1
                )
                events.append((start_frame, end_frame))
                # break
    return remove_overlaps(events)


def detect_turmoil_death(turm_data, pre=10, post=5, fps=30):
    events = []
    for i in range(250, len(turm_data)):
        lives = turm_data[i, 57]
        if turm_data[i - 1, 57] != turm_data[i, 57]:
            start_frame = i - int(pre * fps)
            end_frame = min(
                i + int(post * fps), len(turm_data) - 1
            )
            events.append((start_frame, end_frame))
    return remove_overlaps(events)


def detect_turmoil_prize(turm_data, pre=4, post=7, fps=30):
    events = []
    appear = None  # Frame index where prize first appears
    removed = None  # Frame index where prize disappears

    for i in range(270, len(turm_data)):  # Start checking from frame 250
        obstacles = turm_data[i, 62:69]  # Get the 7 obstacle values

        if 3 in obstacles:  # Prize appears
            if appear is None:
                appear = i  # Record first appearance
        else:  # Prize is missing
            if appear is not None:  # Prize was present before but now gone
                removed = i
                start_frame = max(
                    0, appear - int(pre * fps)
                )  # Ensure start_frame is >= 0
                end_frame = min(
                    removed + int(post * fps), len(turm_data) - 1
                )  # Ensure end_frame is within bounds
                events.append((start_frame, end_frame))

                # Reset for detecting another prize event
                appear = None
                removed = None

    return remove_overlaps(events)
    # break
    return remove_overlaps(events)


# Word Zapper


def detect_word_freebie_use(word_data, pre=5, post=10, fps=30):
    events = []
    for i in range(300, len(word_data)):
        freebie_shots = word_data[i, 96]
        if word_data[i - 1, 96] == 0 and freebie_shots > 0:
            start_frame = i - int(pre * fps)
            end_frame = min(
                i + int(post * fps), len(word_data) - 1
            )
            events.append((start_frame, end_frame))
    return remove_overlaps(events)


def detect_word_letter_stagnation(word_data, stagnation=10, post=3, fps=30):
    events = []
    start_idx = 300
    while start_idx < len(word_data):
        letter_index = word_data[start_idx, 88]
        end_idx = start_idx
        # Extend while scores do not change
        while end_idx < len(word_data) and word_data[end_idx, 88] == letter_index:
            end_idx += 1
        if (end_idx - start_idx) >= stagnation * fps:
            events.append((start_idx, min(len(word_data, end_idx + (post * fps)))))
        start_idx = end_idx
    return remove_overlaps(events)


# %%
