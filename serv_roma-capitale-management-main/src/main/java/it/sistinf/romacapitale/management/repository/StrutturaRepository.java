package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.StrutturaEntity;
import org.springframework.stereotype.Repository;

@Repository
public class StrutturaRepository extends AbstractRepository<Long, StrutturaEntity> {

    public StrutturaRepository() {
        super(StrutturaEntity.class);
    }
}
