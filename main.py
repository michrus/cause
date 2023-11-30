import secrets
from datetime import timedelta

from src.frameworks_and_drivers.server.flask_router import app, g

from src.adapters.api_presenter import ApiAuthTokenPresenter
from src.adapters.database.multi_database import MultiDatabaseAccess
from src.adapters.username_password_controller import UsernamePasswordController
from src.application.use_cases.username_password_auth \
    import UsernamePasswordAuthInteractor
from src.frameworks_and_drivers.database.sqlite3_db \
    import LowLevelEagerSQLite3Database
from src.frameworks_and_drivers.token.jwt_token import JWTTokenGenerator


if __name__ == "__main__":

    user_db_access = LowLevelEagerSQLite3Database(db_name="user.db",
                                                  db_dir_path="./")
    hash_db_access = LowLevelEagerSQLite3Database(db_name="hash.db",
                                                  db_dir_path="./")
    multi_database_access = MultiDatabaseAccess(user_data_access=user_db_access,
                                                user_data_table="user_data",
                                                user_hash_access=hash_db_access,
                                                user_hash_table="user_hash")

    secrets_hex = secrets.token_hex(32)
    one_hour = timedelta(hours=1)
    jwt_generator = JWTTokenGenerator(secret_key=secrets_hex,
                                      expiration_period=one_hour)

    presenter = ApiAuthTokenPresenter()
    username_password_interactor = UsernamePasswordAuthInteractor(
        data_access=multi_database_access,
        token_generator=jwt_generator,
        presenter=presenter
    )
    controller = UsernamePasswordController(
        use_case=username_password_interactor
    )

    g.controller = controller

    app.run(debug=True)
