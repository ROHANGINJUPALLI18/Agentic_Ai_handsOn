import traceback
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob, Options
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def _get_required_env(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"Missing required environment variable: {name}")
	return value


def _validate_videosdk_auth_token(token: str) -> str:
	if token.count(".") != 2:
		raise RuntimeError(
			"Invalid VIDEOSDK_AUTH_TOKEN. Expected a VideoSDK auth JWT (3 dot-separated parts). "
			"Generate a valid token from VideoSDK dashboard/auth API and set it in 03/AI_Calls_Agent/.env"
		)
	return token

# Define the agent's behavior and personality
class MyVoiceAgent(Agent):
	def __init__(self):
		super().__init__(
			instructions="You are a helpful AI assistant that answers phone calls. Keep your responses concise and friendly.",
		)

	async def on_enter(self) -> None:
		await self.session.say("Hello! I'm your real-time assistant. How can I help you today?")

	async def on_exit(self) -> None:
		return

async def start_session(context: JobContext):
	# Configure the Gemini model for real-time voice
	google_api_key = _get_required_env("GOOGLE_API_KEY")
	model = GeminiRealtime(
		model="gemini-2.5-flash-native-audio-preview-12-2025",
		api_key=google_api_key,
		config=GeminiLiveConfig(
			voice="Leda",
			response_modalities=["AUDIO"]
		)
	)
	pipeline = RealTimePipeline(model=model)
	session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

	await context.connect()
	await context.run_until_shutdown(session=session, wait_for_participant=True)

def make_context() -> JobContext:
	room_options = RoomOptions()
	return JobContext(room_options=room_options)

if __name__ == "__main__":
	try:
		videosdk_auth_token = _validate_videosdk_auth_token(_get_required_env("VIDEOSDK_AUTH_TOKEN"))

		# Register the agent with a unique ID
		options = Options(
			agent_id="MyTelephonyAgent", # CRITICAL: Unique identifier for routing
			auth_token=videosdk_auth_token,
			register=True, # REQUIRED: Register with VideoSDK for telephony
			max_processes=10, # Concurrent calls to handle
			host="localhost",
			port=8081,
		)
		job = WorkerJob(entrypoint=start_session, jobctx=make_context, options=options)
		job.start()
	except Exception as e:
		traceback.print_exc()