from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import cast, Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship  # , DeclarativeBase


Base = declarative_base()


class ReferenceSite(Base):
    __tablename__ = 'reference_sites'

    id = Column(Integer, unique=True, primary_key=True,
                autoincrement=True)
    site_name = Column(String(30), unique=True, )
    wavelengths = Column(postgresql.ARRAY(Float))
    band_names = Column(postgresql.ARRAY(String))
    default_quicklook = Column(String)

    def __repr__(self):
        return "<ReferenceSite(id='{}', site_name='{}', wavelengths={}, band_names={}, default_quicklook='{}')>" \
            .format(self.id, self.site_name, self.wavelengths, self.band_names, self.default_quicklook)


class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    collection = Column(String(30), unique=True)
    wavelengths = Column(postgresql.ARRAY(Float))
    band_names = Column(postgresql.ARRAY(String))

    def __repr__(self):
        return "<Collection(id='{}', collection='{}', wavelengths={}, band_names={})>" \
            .format(self.id, self.collection, self.wavelengths, self.band_names)


class Matchup(Base):
    __tablename__ = 'matchups'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    sensor_1_collection_id = Column(Integer, ForeignKey("collections.id", onupdate='CASCADE', ondelete='CASCADE'),
                                    nullable=False)
    sensor_2_collection_id = Column(Integer, ForeignKey("collections.id", onupdate='CASCADE', ondelete='CASCADE'),
                                    nullable=True)
    sensor_2_reference_id = Column(Integer, ForeignKey("reference_sites.id", onupdate='CASCADE', ondelete='CASCADE'),
                                   nullable=True)
    timediff = Column(Float, nullable=False)
    full_sensor_1_prod_name = Column(String, nullable=False)
    full_sensor_2_prod_name = Column(String, nullable=False)
    sensor_1_bands = Column(postgresql.ARRAY(String), nullable=False)
    sensor_2_bands = Column(postgresql.ARRAY(String), nullable=True)
    sensor_1_wavelengths = Column(postgresql.ARRAY(String), nullable=False)
    product_date = Column(DateTime)
    quick_look = Column(String)
    AOD = Column(Float)
    pressure = Column(Float)
    H2O = Column(Float)
    O3 = Column(Float)
    temp = Column(Float)
    sensor1_id = Column(String)
    sensor1_tile_cloud_percentage = Column(Float)
    sensor1_sat_azimuth = Column(Float)
    sensor1_sun_azimuth = Column(Float)
    sensor1_sun_elevation = Column(Float)
    sensor1_view_angle = Column(Float)

    reference = relationship("ReferenceSite", foreign_keys=[sensor_2_reference_id])
    collection_1 = relationship("Collection", foreign_keys=[sensor_1_collection_id])
    collection_2 = relationship("Collection", foreign_keys=[sensor_2_collection_id])

    # defines output when called
    def __repr__(self):
        if self.sensor_2_reference_id is not None:
            return ("<Matchup(id='{}', sensor_1_collection_id='{}', sensor_2_reference_id='{}', timediff={}, "
                    "full_sensor_1_prod_name={}, full_sensor_2_prod_name={}, sensor_1_bands={}, sensor_2_bands={}, "
                    "sensor_1_wavelengths={}, product_date={}, quick_look={}, AOD={}, pressure={}, H2O={}, O3={}, temp={}"
                    "sensor1_id={}, sensor1_tile_cloud_percentage={}, sensor1_sat_azimuth={}, sensor1_sun_azimuth={}, sensor1_sun_elevation={}"
                    "sensor1_view_angle={}"
                    .format(self.id, self.sensor_1_collection_id, self.sensor_2_reference_id, self.timediff,
                            self.full_sensor_1_prod_name, self.full_sensor_2_prod_name, self.sensor_1_bands,
                            self.sensor_2_bands, self.sensor_1_wavelengths, self.product_date, self.quick_look,
                            self.AOD, self.pressure, self.H2O, self.O3, self.temp,
                            self.sensor1_id, self.sensor1_tile_cloud_percentage, self.sensor1_sat_azimuth,
                            self.sensor1_sun_azimuth, self.sensor1_sun_elevation, self.sensor1_view_angle))
        elif self.sensor_2_collection_id is not None:
            return ("<Matchup(id='{}', sensor_1_collection_id='{}', sensor_2_collection_id='{}', timediff={}, "
                    "full_sensor_1_prod_name={}, full_sensor_2_prod_name={}, sensor_1_bands={}, sensor_2_bands={}, "
                    "sensor_1_wavelengths={}, product_date={}, quick_look={}, AOD={}, pressure={}, H2O={}, O3={}, temp={}"
                    "sensor1_id={}, sensor1_tile_cloud_percentage={}, sensor1_sat_azimuth={}, sensor1_sun_azimuth={}, sensor1_sun_elevation={}"
                    "sensor1_view_angle={}"
                    .format(self.id, self.sensor_1_collection_id, self.sensor_2_collection_id, self.timediff,
                            self.full_sensor_1_prod_name, self.full_sensor_2_prod_name, self.sensor_1_bands,
                            self.sensor_2_bands, self.sensor_1_wavelengths, self.product_date, self.quick_look,
                            self.AOD, self.pressure, self.H2O, self.O3, self.temp,
                            self.sensor1_id, self.sensor1_tile_cloud_percentage, self.sensor1_sat_azimuth,
                            self.sensor1_sun_azimuth, self.sensor1_sun_elevation, self.sensor1_view_angle))


class BiasVals(Base):
    __tablename__ = 'bias_vals'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    matchup_id = Column(Integer, ForeignKey("matchups.id", onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    band_1 = Column(postgresql.ARRAY(Float))
    band_2 = Column(postgresql.ARRAY(Float))
    band_3 = Column(postgresql.ARRAY(Float))
    band_4 = Column(postgresql.ARRAY(Float))
    band_5 = Column(postgresql.ARRAY(Float))
    band_6 = Column(postgresql.ARRAY(Float))
    band_7 = Column(postgresql.ARRAY(Float))
    band_8 = Column(postgresql.ARRAY(Float))
    band_9 = Column(postgresql.ARRAY(Float))
    band_10 = Column(postgresql.ARRAY(Float))
    band_11 = Column(postgresql.ARRAY(Float))
    band_12 = Column(postgresql.ARRAY(Float))
    band_13 = Column(postgresql.ARRAY(Float))

    matchup = relationship("Matchup", foreign_keys=[matchup_id])

    def __repr__(self):
        return "<BiasVals(matchup_id={}, band_1={}, band_2={}, band_3={}, band_4={}, band_5={}, band_6={}, band_7={}," \
               " band_8={}, band_9={}, band_10={}, band_11={}, band_12={}, band_13={}>" \
            .format(self.matchup_id, self.band_1, self.band_2, self.band_3, self.band_4, self.band_5, self.band_6,
                    self.band_7, self.band_8, self.band_9, self.band_10, self.band_11, self.band_12, self.band_13)


class BiasUncVals(Base):
    __tablename__ = 'bias_unc_vals'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    matchup_id = Column(Integer, ForeignKey("matchups.id", onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    band_1 = Column(postgresql.ARRAY(Float))
    band_2 = Column(postgresql.ARRAY(Float))
    band_3 = Column(postgresql.ARRAY(Float))
    band_4 = Column(postgresql.ARRAY(Float))
    band_5 = Column(postgresql.ARRAY(Float))
    band_6 = Column(postgresql.ARRAY(Float))
    band_7 = Column(postgresql.ARRAY(Float))
    band_8 = Column(postgresql.ARRAY(Float))
    band_9 = Column(postgresql.ARRAY(Float))
    band_10 = Column(postgresql.ARRAY(Float))
    band_11 = Column(postgresql.ARRAY(Float))
    band_12 = Column(postgresql.ARRAY(Float))
    band_13 = Column(postgresql.ARRAY(Float))

    matchup = relationship("Matchup", foreign_keys=[matchup_id])

    def __repr__(self):
        return "<BiasUncVals(matchup_id={}, band_1={}, band_2={}, band_3={}, band_4={}, band_5={}, band_6={}, band_7={}," \
               " band_8={}, band_9={}, band_10={}, band_11={}, band_12={}, band_13={}>" \
            .format(self.matchup_id, self.band_1, self.band_2, self.band_3, self.band_4, self.band_5, self.band_6,
                    self.band_7, self.band_8, self.band_9, self.band_10, self.band_11, self.band_12, self.band_13)


class MeasVals(Base):
    __tablename__ = 'meas_vals'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    matchup_id = Column(Integer, ForeignKey("matchups.id", onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    sensor_1_collection_id = Column(Integer, ForeignKey("collections.id", onupdate='CASCADE', ondelete='CASCADE'),
                                    nullable=True)
    sensor_2_collection_id = Column(Integer, ForeignKey("collections.id", onupdate='CASCADE', ondelete='CASCADE'),
                                    nullable=True)
    sensor_2_reference_id = Column(Integer, ForeignKey("reference_sites.id", onupdate='CASCADE', ondelete='CASCADE'),
                                   nullable=True)
    measurand = Column(String)
    band_1 = Column(postgresql.ARRAY(Float))
    band_2 = Column(postgresql.ARRAY(Float))
    band_3 = Column(postgresql.ARRAY(Float))
    band_4 = Column(postgresql.ARRAY(Float))
    band_5 = Column(postgresql.ARRAY(Float))
    band_6 = Column(postgresql.ARRAY(Float))
    band_7 = Column(postgresql.ARRAY(Float))
    band_8 = Column(postgresql.ARRAY(Float))
    band_9 = Column(postgresql.ARRAY(Float))
    band_10 = Column(postgresql.ARRAY(Float))
    band_11 = Column(postgresql.ARRAY(Float))
    band_12 = Column(postgresql.ARRAY(Float))
    band_13 = Column(postgresql.ARRAY(Float))

    matchup = relationship("Matchup", foreign_keys=[matchup_id])
    reference = relationship("ReferenceSite", foreign_keys=[sensor_2_reference_id])
    collection_1 = relationship("Collection", foreign_keys=[sensor_1_collection_id])
    collection_2 = relationship("Collection", foreign_keys=[sensor_2_collection_id])

    def __repr__(self):
        if self.sensor_2_reference_id is not None:
            return "<MeasVals(matchup_id={}, measurand={}, sensor_2_reference_id='{}', band_1={}, band_2={}, band_3={}, band_4={}, band_5={}, band_6={}, band_7={}," \
                   " band_8={}, band_9={}, band_10={}, band_11={}, band_12={}, band_13={}>" \
                .format(self.matchup_id, self.measurand, self.sensor_2_reference_id,
                        self.band_1, self.band_2, self.band_3, self.band_4, self.band_5, self.band_6,
                        self.band_7, self.band_8, self.band_9, self.band_10, self.band_11, self.band_12, self.band_13)
        elif self.sensor_2_collection_id is not None:
            return "<MeasVals(matchup_id={}, measurand={}, sensor_2_collection_id='{}',band_1={}, band_2={}, band_3={}, band_4={}, band_5={}, band_6={}, band_7={}," \
                   " band_8={}, band_9={}, band_10={}, band_11={}, band_12={}, band_13={}>" \
                .format(self.matchup_id, self.measurand,self.sensor_2_collection_id,
                        self.band_1, self.band_2, self.band_3, self.band_4, self.band_5, self.band_6,
                        self.band_7, self.band_8, self.band_9, self.band_10, self.band_11, self.band_12, self.band_13)
        elif self.sensor_1_collection_id is not None:
            return "<MeasVals(matchup_id={}, measurand={}, sensor_1_collection_id='{}', band_1={}, band_2={}, band_3={}, band_4={}, band_5={}, band_6={}, band_7={}," \
                   " band_8={}, band_9={}, band_10={}, band_11={}, band_12={}, band_13={}>" \
                .format(self.matchup_id, self.measurand, self.sensor_1_collection_id,
                        self.band_1, self.band_2, self.band_3, self.band_4, self.band_5, self.band_6,
                        self.band_7, self.band_8, self.band_9, self.band_10, self.band_11, self.band_12, self.band_13)
