from __future__ import annotations

from uuid import uuid4
from .spritesheet import SpriteSheet

class SpriteAnimation(object):
	"""A sprite sheet animation composes an animation from frames all defined within a single sprite sheet.
	The sprite sheet has to be initialized to provide access to all image content.
	"""
	def __init__(self, sprite_sheet:SpriteSheet, name:str=None, frames:list = None, fps:int=24, repeats:bool=False):
		"""Generate a new Sprite sheet based animation.

		Args:
				sprite_sheet (SpriteSheet): the sprite source from where animation frames are taken
				name (str): Name of the animation (optional) - if not provided the internal id is used.				
				frames (list, optional): optional list of sprite names to initialize the animation
				repeats (bool, optional): Whether this is a cyclic animation or not. Defaults to False.

		Raises:
				ValueError: [description]
		"""
		super(SpriteAnimation, self).__init__()
		self._id = uuid4()
		self._name = name if name else self._id
		self._current_frame = 0		
		self._source  = sprite_sheet
		self._repeats = repeats
		self._frames  = []
		self._start_index = 0
		self._end_index   = 0
		self._frames_per_second = fps
		self._frame_hold = 1000. / fps
		self._frame_elapsed = 0.

		if frames:
			for n in frames:
				self.add_frame(n)

	@property
	def current_frame(self):
		return self._current_frame

	@property
	def repeats(self):
		return self._repeats

	@property
	def no_frames(self):
		return len(self._frames)

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name

	def add_frame(self, name:str):
		if self._source == None:
			raise ValueError("No Sprite Sheet Provided")

		if name not in self._source.sprite_names:
			raise ValueError("No Sprite with that name registered in source")

		self._frames.append(self._source[name])
		self._end_index = len(self._frames) - 1

		return self

	def __iter__(self):
		return self._frames.__iter__()

	def reset(self):
		self._frame_elapsed = 0.
		self._current_frame = self._start_index

	def update(self, delta_time:float):
		if len(self._frames) == 0:
			raise ValueError("No frames registered")

		i_current_frame = self._current_frame

		# only if the clock gave a tick that makes our frame update, only then do we move to the next frame
		self._frame_elapsed += delta_time
		if self._frame_elapsed >= self._frame_hold:
			
			self._current_frame += 1
			if self._current_frame == self._end_index + 1:
				if self._repeats:
					self.reset()
				else:
					self._current_frame = i_current_frame

			# update our clock
			self._frame_elapsed -= self._frame_hold

		return self._frames[i_current_frame]


	def next(self, delta_time:float):
		return self.update(delta_time)

	def delete_frame(self, frame:int):		
		if len(self._frames) == 0:
			raise ValueError("No frame to delete")

		if not (0 <= frame <= len(self._frames) - 1):
			raise ValueError("Frame cannot be less than 0 and greater then length")

		del self._frames[frame]
		self._end_index = len(self._frames) - 1

		return self

	@property
	def start_index(self):
		return self._start_index

	@start_index.setter
	def start_index(self, v:int):
		if not 0 <= v < self.no_frames:
			raise ValueError("start index cannot be outside of the frames")
		if v > self._end_index:
			raise ValueError("start index > end index")
		self._start_index = v
		return self

	@property
	def end_index(self):
		return self._end_index

	@end_index.setter
	def end_index(self, v):
		if not 0 <= v < self.no_frames:
			raise ValueError("end index cannot be outside of the frames")
		if v < self._end_index:
			raise ValueError("end index < start index")
		self._start_index = v
		return self

	@property
	def to_json(self, exclude_fields:list=['_id', '_current_frame']):
		raise ValueError("Not Implemented")

	def __repr__(self):
		return "Animation-{}({})".format(self._name, self._id)