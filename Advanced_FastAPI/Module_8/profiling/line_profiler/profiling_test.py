from app import process_data
# profilng
@profile
def run():
    process_data(10000)


if __name__=='__main__':
    run()


# To run the line profiler
# kernprof -l -v profiling_test.py
# It will not work with uvicorn it is having its own kernel "kernprof" that why seperate file is being created
