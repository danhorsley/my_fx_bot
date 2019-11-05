import pandas as pd
import numpy as np
from .models import *

eurusd_array = np.array(DB.session.query(EURUSD.date,EURUSD.price).all())

