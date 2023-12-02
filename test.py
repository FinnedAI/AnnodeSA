import twint

# Configure
c = twint.Config()
c.Search = "great"

# Run
twint.run.Search(c)
